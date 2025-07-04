// ArticlesDataTable.tsx - Advanced Medical Articles Data Table
// High-impact component with search, filters, sorting, and dual-mode support

import React, { useState, useMemo } from 'react';
import { useDualMode } from '../../contexts/DualModeContext';
import { Article } from '../../types/medical';

interface ArticlesDataTableProps {
  articles: Article[];
  loading?: boolean;
  className?: string;
}

interface FilterState {
  search: string;
  sentiment: string;
  topic: string;
  source: string;
  country: string;
}

export const ArticlesDataTable: React.FC<ArticlesDataTableProps> = ({
  articles,
  loading = false,
  className = ''
}) => {
  const { currentMode } = useDualMode();
  const isProfessional = currentMode === 'professional';

  // State management
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [sortField, setSortField] = useState<keyof Article>('published_at');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [filters, setFilters] = useState<FilterState>({
    search: '',
    sentiment: '',
    topic: '',
    source: '',
    country: ''
  });

  // Get unique values for filters
  const uniqueValues = useMemo(() => ({
    sentiments: [...new Set(articles.map(a => a.sentiment_label).filter(Boolean))],
    topics: [...new Set(articles.map(a => a.topic_category).filter(Boolean))],
    sources: [...new Set(articles.map(a => a.source?.name).filter(Boolean))],
    countries: [...new Set(articles.map(a => a.country).filter(Boolean))]
  }), [articles]);

  // Filter and sort articles
  const filteredAndSortedArticles = useMemo(() => {
    const filtered = articles.filter(article => {
      const matchesSearch = !filters.search ||
        article.title.toLowerCase().includes(filters.search.toLowerCase()) ||
        article.summary?.toLowerCase().includes(filters.search.toLowerCase());

      const matchesSentiment = !filters.sentiment || article.sentiment_label === filters.sentiment;
      const matchesTopic = !filters.topic || article.topic_category === filters.topic;
      const matchesSource = !filters.source || article.source?.name === filters.source;
      const matchesCountry = !filters.country || article.country === filters.country;

      return matchesSearch && matchesSentiment && matchesTopic && matchesSource && matchesCountry;
    });

    // Sort articles
    filtered.sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];

      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;

      let comparison = 0;
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        comparison = aVal.localeCompare(bVal);
      } else if (typeof aVal === 'number' && typeof bVal === 'number') {
        comparison = aVal - bVal;
      } else {
        comparison = String(aVal).localeCompare(String(bVal));
      }

      return sortDirection === 'asc' ? comparison : -comparison;
    });

    return filtered;
  }, [articles, filters, sortField, sortDirection]);

  // Pagination
  const totalPages = Math.ceil(filteredAndSortedArticles.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedArticles = filteredAndSortedArticles.slice(startIndex, startIndex + itemsPerPage);

  // Handlers
  const handleSort = (field: keyof Article) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1); // Reset to first page
  };

  const clearFilters = () => {
    setFilters({
      search: '',
      sentiment: '',
      topic: '',
      source: '',
      country: ''
    });
    setCurrentPage(1);
  };

  const getSentimentColor = (sentiment: string | undefined) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      case 'neutral': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-500 bg-gray-50';
    }
  };

  const getTopicColor = (topic: string | undefined) => {
    const colors: Record<string, string> = {
      treatment: 'text-blue-600 bg-blue-100',
      research: 'text-purple-600 bg-purple-100',
      diagnosis: 'text-orange-600 bg-orange-100',
      surgery: 'text-red-600 bg-red-100',
      genetics: 'text-indigo-600 bg-indigo-100',
      general: 'text-gray-600 bg-gray-100'
    };
    return colors[topic || ''] || 'text-gray-500 bg-gray-50';
  };

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-12 bg-gray-200 rounded"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-lg ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h3 className="text-xl font-semibold text-gray-900">
              {isProfessional ? 'Medical Articles Database' : 'Health News Articles'}
            </h3>
            <p className="text-sm text-gray-600">
              {isProfessional
                ? `${filteredAndSortedArticles.length} articles from ${uniqueValues.sources.length} medical sources`
                : `${filteredAndSortedArticles.length} health news articles to explore`
              }
            </p>
          </div>
          <button
            onClick={clearFilters}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Clear Filters
          </button>
        </div>

        {/* Search and Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {/* Search */}
          <div className="lg:col-span-2">
            <input
              type="text"
              placeholder={isProfessional ? "Search articles by title or content..." : "Search for health topics..."}
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Sentiment Filter */}
          <select
            value={filters.sentiment}
            onChange={(e) => handleFilterChange('sentiment', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Sentiments</option>
            {uniqueValues.sentiments.map(sentiment => (
              <option key={sentiment} value={sentiment}>
                {sentiment ? sentiment.charAt(0).toUpperCase() + sentiment.slice(1) : 'Unknown'}
              </option>
            ))}
          </select>

          {/* Topic Filter */}
          <select
            value={filters.topic}
            onChange={(e) => handleFilterChange('topic', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Topics</option>
            {uniqueValues.topics.map(topic => (
              <option key={topic} value={topic}>
                {topic ? topic.charAt(0).toUpperCase() + topic.slice(1) : 'General'}
              </option>
            ))}
          </select>

          {/* Source Filter */}
          <select
            value={filters.source}
            onChange={(e) => handleFilterChange('source', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Sources</option>
            {uniqueValues.sources.map(source => (
              <option key={source} value={source}>
                {source}
              </option>
            ))}
          </select>

          {/* Country Filter */}
          <select
            value={filters.country}
            onChange={(e) => handleFilterChange('country', e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Countries</option>
            {uniqueValues.countries.map(country => (
              <option key={country} value={country}>
                {country}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th
                onClick={() => handleSort('title')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                Title {sortField === 'title' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => handleSort('source')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                Source {sortField === 'source' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => handleSort('sentiment_label')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                Sentiment {sortField === 'sentiment_label' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => handleSort('topic_category')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                Topic {sortField === 'topic_category' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => handleSort('published_at')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                Date {sortField === 'published_at' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              <th
                onClick={() => handleSort('country')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                Country {sortField === 'country' && (sortDirection === 'asc' ? '↑' : '↓')}
              </th>
              {isProfessional && (
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Score
                </th>
              )}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedArticles.map((article) => (
              <tr key={article.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="max-w-xs">
                    <div className="text-sm font-medium text-gray-900 truncate">
                      {article.title}
                    </div>
                    {article.summary && (
                      <div className="text-sm text-gray-500 mt-1 line-clamp-2">
                        {article.summary}
                      </div>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{article.source?.name}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getSentimentColor(article.sentiment_label || '')}`}>
                    {article.sentiment_label || 'Unknown'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getTopicColor(article.topic_category || '')}`}>
                    {article.topic_category || 'General'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {article.published_at ? new Date(article.published_at).toLocaleDateString() : 'Unknown'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {article.country}
                </td>
                {isProfessional && (
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {article.sentiment_score?.toFixed(3) || 'N/A'}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="px-6 py-3 border-t border-gray-200 flex items-center justify-between">
        <div className="text-sm text-gray-700">
          Showing {startIndex + 1} to {Math.min(startIndex + itemsPerPage, filteredAndSortedArticles.length)} of {filteredAndSortedArticles.length} articles
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-md">
            {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>

      {/* Educational Mode Help */}
      {!isProfessional && (
        <div className="px-6 py-4 bg-blue-50 border-t border-blue-200">
          <div className="text-sm text-blue-800">
            <strong>💡 How to use:</strong> Use the search box to find articles about specific health topics.
            Filter by sentiment to see positive/negative news, or by topic to explore different medical areas.
          </div>
        </div>
      )}
    </div>
  );
};

export default ArticlesDataTable;
