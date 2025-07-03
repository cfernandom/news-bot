// ArticlesTableSection.tsx - Articles Data Table Integration for Dashboard
// Connects ArticlesDataTable with API data and dual-mode context

import React from 'react';
import { ArticlesDataTable } from '../tables/ArticlesDataTable';
import { useMedicalArticles } from '../../hooks/useMedicalData';
import { useDualMode } from '../../contexts/DualModeContext';

interface ArticlesTableSectionProps {
  className?: string;
}

export const ArticlesTableSection: React.FC<ArticlesTableSectionProps> = ({
  className = ''
}) => {
  const { currentMode } = useDualMode();
  const isProfessional = currentMode === 'professional';

  // Fetch articles data with appropriate limit for performance
  const { data, isLoading, error } = useMedicalArticles({
    limit: isProfessional ? 200 : 50 // Professional mode shows more data
  });

  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-lg p-6 ${className}`}>
        <div className="text-red-800">
          <h3 className="text-lg font-semibold mb-2">
            {isProfessional ? 'Medical Data Error' : 'Unable to Load Articles'}
          </h3>
          <p className="text-sm">
            {isProfessional
              ? 'Failed to retrieve medical articles from the database. Please check system connectivity.'
              : 'We\'re having trouble loading the health news articles. Please try again later.'
            }
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Section Header with Dual-Mode Context */}
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">
          {isProfessional ? 'Medical Articles Database' : 'Health News Explorer'}
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          {isProfessional
            ? 'Comprehensive database of medical articles with advanced filtering, sentiment analysis, and topic classification for research purposes.'
            : 'Explore the latest health news articles. Search, filter, and discover information about breast cancer research and treatment.'
          }
        </p>
      </div>

      {/* Articles Data Table */}
      <ArticlesDataTable
        articles={(data?.articles || []) as any[]}
        loading={isLoading}
        className="shadow-lg"
      />

      {/* Educational Mode Additional Info */}
      {!isProfessional && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">
            Understanding the Data 📊
          </h3>
          <div className="text-sm text-blue-800 space-y-2">
            <p>
              <strong>Sentiment:</strong> Shows whether an article presents positive, negative, or neutral information about medical topics.
            </p>
            <p>
              <strong>Topics:</strong> Articles are categorized into areas like treatment, research, diagnosis, surgery, and more.
            </p>
            <p>
              <strong>Sources:</strong> Articles come from trusted medical news websites and research publications.
            </p>
            <p>
              <strong>Country:</strong> Indicates the geographic focus or origin of the medical news.
            </p>
          </div>
        </div>
      )}

      {/* Professional Mode Statistics */}
      {isProfessional && data && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Dataset Statistics
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{data.total}</div>
              <div className="text-gray-600">Total Articles</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {data.articles.filter((a: any) => a.sentiment_label === 'positive').length}
              </div>
              <div className="text-gray-600">Positive Sentiment</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {data.articles.filter((a: any) => a.sentiment_label === 'negative').length}
              </div>
              <div className="text-gray-600">Negative Sentiment</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {new Set(data.articles.map((a: any) => a.topic_category)).size}
              </div>
              <div className="text-gray-600">Topic Categories</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ArticlesTableSection;
