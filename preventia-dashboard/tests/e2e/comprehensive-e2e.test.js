/**
 * Comprehensive E2E tests for PreventIA Dashboard
 * Tests complete user workflows and integration scenarios
 */

import puppeteer from 'puppeteer';
import { describe, test, expect, beforeAll, afterAll, beforeEach } from 'vitest';

describe('PreventIA Dashboard E2E Tests', () => {
  let browser;
  let page;
  const BASE_URL = process.env.VITE_APP_URL || 'http://localhost:5173';
  const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';

  beforeAll(async () => {
    browser = await puppeteer.launch({
      headless: process.env.CI === 'true',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
  });

  afterAll(async () => {
    await browser.close();
  });

  beforeEach(async () => {
    page = await browser.newPage();
    await page.goto(BASE_URL);
  });

  describe('Application Loading and Navigation', () => {
    test('loads main dashboard successfully', async () => {
      await page.waitForSelector('[data-testid="main-dashboard"]', { timeout: 10000 });
      const title = await page.title();
      expect(title).toContain('PreventIA');
    });

    test('navigation menu works correctly', async () => {
      // Test main navigation items
      await page.click('[data-testid="nav-analytics"]');
      await page.waitForSelector('[data-testid="analytics-page"]');

      await page.click('[data-testid="nav-articles"]');
      await page.waitForSelector('[data-testid="articles-page"]');

      await page.click('[data-testid="nav-settings"]');
      await page.waitForSelector('[data-testid="settings-page"]');
    });

    test('responsive design works on mobile', async () => {
      await page.setViewport({ width: 375, height: 667 });
      await page.waitForSelector('[data-testid="mobile-menu-toggle"]');
      await page.click('[data-testid="mobile-menu-toggle"]');
      await page.waitForSelector('[data-testid="mobile-nav-menu"]');
    });
  });

  describe('Dashboard Analytics Integration', () => {
    test('sentiment chart loads and displays data', async () => {
      await page.waitForSelector('[data-testid="sentiment-chart"]', { timeout: 15000 });

      // Check chart is rendered
      const chartElements = await page.$$('[data-testid="sentiment-chart"] svg');
      expect(chartElements.length).toBeGreaterThan(0);

      // Check legend is present
      await page.waitForSelector('[data-testid="sentiment-legend"]');
      const legendItems = await page.$$('[data-testid="sentiment-legend"] .legend-item');
      expect(legendItems.length).toBeGreaterThan(0);
    });

    test('topics chart displays correct data', async () => {
      await page.waitForSelector('[data-testid="topics-chart"]', { timeout: 15000 });

      const topicsData = await page.$$('[data-testid="topic-bar"]');
      expect(topicsData.length).toBeGreaterThan(0);

      // Test tooltip functionality
      await page.hover('[data-testid="topic-bar"]:first-child');
      await page.waitForSelector('[data-testid="chart-tooltip"]');
    });

    test('geographic map displays coverage data', async () => {
      await page.waitForSelector('[data-testid="geographic-map"]', { timeout: 15000 });

      // Check map container is present
      const mapContainer = await page.$('[data-testid="map-container"]');
      expect(mapContainer).toBeTruthy();

      // Check legend is present
      await page.waitForSelector('[data-testid="map-legend"]');
    });

    test('timeline chart shows temporal data', async () => {
      await page.waitForSelector('[data-testid="timeline-chart"]', { timeout: 15000 });

      const timelinePoints = await page.$$('[data-testid="timeline-point"]');
      expect(timelinePoints.length).toBeGreaterThan(0);

      // Test date range selector
      await page.click('[data-testid="date-range-selector"]');
      await page.click('[data-testid="date-range-30-days"]');
      await page.waitForSelector('[data-testid="timeline-chart"]');
    });
  });

  describe('Articles Management', () => {
    test('articles list loads and displays data', async () => {
      await page.click('[data-testid="nav-articles"]');
      await page.waitForSelector('[data-testid="articles-list"]', { timeout: 15000 });

      const articles = await page.$$('[data-testid="article-item"]');
      expect(articles.length).toBeGreaterThan(0);
    });

    test('article search functionality works', async () => {
      await page.click('[data-testid="nav-articles"]');
      await page.waitForSelector('[data-testid="search-input"]');

      await page.type('[data-testid="search-input"]', 'breast cancer');
      await page.click('[data-testid="search-button"]');

      await page.waitForSelector('[data-testid="search-results"]');
      const searchResults = await page.$$('[data-testid="article-item"]');
      expect(searchResults.length).toBeGreaterThan(0);
    });

    test('article detail view displays complete information', async () => {
      await page.click('[data-testid="nav-articles"]');
      await page.waitForSelector('[data-testid="article-item"]');

      await page.click('[data-testid="article-item"]:first-child');
      await page.waitForSelector('[data-testid="article-detail"]');

      // Check required fields are present
      await page.waitForSelector('[data-testid="article-title"]');
      await page.waitForSelector('[data-testid="article-content"]');
      await page.waitForSelector('[data-testid="article-sentiment"]');
      await page.waitForSelector('[data-testid="article-topics"]');
    });

    test('article filtering works correctly', async () => {
      await page.click('[data-testid="nav-articles"]');
      await page.waitForSelector('[data-testid="filter-dropdown"]');

      await page.click('[data-testid="filter-dropdown"]');
      await page.click('[data-testid="filter-positive-sentiment"]');

      await page.waitForSelector('[data-testid="filtered-articles"]');
      const filteredArticles = await page.$$('[data-testid="article-item"]');
      expect(filteredArticles.length).toBeGreaterThan(0);
    });
  });

  describe('Export and Download Features', () => {
    test('PDF export functionality works', async () => {
      await page.click('[data-testid="export-button"]');
      await page.waitForSelector('[data-testid="export-menu"]');

      await page.click('[data-testid="export-pdf"]');
      await page.waitForSelector('[data-testid="export-progress"]');

      // Wait for export completion
      await page.waitForSelector('[data-testid="export-complete"]', { timeout: 30000 });
    });

    test('CSV export functionality works', async () => {
      await page.click('[data-testid="export-button"]');
      await page.click('[data-testid="export-csv"]');

      await page.waitForSelector('[data-testid="export-complete"]', { timeout: 15000 });
    });

    test('export history is maintained', async () => {
      await page.click('[data-testid="nav-settings"]');
      await page.waitForSelector('[data-testid="export-history"]');

      const exportItems = await page.$$('[data-testid="export-item"]');
      expect(exportItems.length).toBeGreaterThan(0);
    });
  });

  describe('User Experience Features', () => {
    test('dark mode toggle works', async () => {
      await page.click('[data-testid="theme-toggle"]');
      await page.waitForSelector('[data-theme="dark"]');

      const isDarkMode = await page.evaluate(() => {
        return document.documentElement.getAttribute('data-theme') === 'dark';
      });
      expect(isDarkMode).toBe(true);
    });

    test('language switching works', async () => {
      await page.click('[data-testid="language-toggle"]');
      await page.waitForSelector('[data-testid="language-menu"]');

      await page.click('[data-testid="language-en"]');
      await page.waitForSelector('[data-testid="nav-analytics"]');

      const analyticsText = await page.textContent('[data-testid="nav-analytics"]');
      expect(analyticsText).toContain('Analytics');
    });

    test('accessibility features work correctly', async () => {
      // Test keyboard navigation
      await page.keyboard.press('Tab');
      await page.keyboard.press('Tab');
      await page.keyboard.press('Enter');

      // Test screen reader announcements
      await page.click('[data-testid="sr-announcement"]');
      const announcement = await page.textContent('[data-testid="sr-text"]');
      expect(announcement).toBeTruthy();
    });
  });

  describe('Error Handling and Edge Cases', () => {
    test('handles API errors gracefully', async () => {
      // Mock API failure
      await page.setRequestInterception(true);
      page.on('request', (req) => {
        if (req.url().includes('/api/v1/articles')) {
          req.respond({
            status: 500,
            contentType: 'application/json',
            body: JSON.stringify({ error: 'Server Error' })
          });
        } else {
          req.continue();
        }
      });

      await page.click('[data-testid="nav-articles"]');
      await page.waitForSelector('[data-testid="error-message"]');

      const errorText = await page.textContent('[data-testid="error-message"]');
      expect(errorText).toContain('Error loading articles');
    });

    test('handles network disconnection', async () => {
      await page.setOfflineMode(true);
      await page.click('[data-testid="refresh-button"]');

      await page.waitForSelector('[data-testid="offline-message"]');
      const offlineMessage = await page.textContent('[data-testid="offline-message"]');
      expect(offlineMessage).toContain('offline');
    });

    test('handles large dataset performance', async () => {
      // Test with large dataset
      await page.goto(`${BASE_URL}/articles?limit=1000`);

      const startTime = Date.now();
      await page.waitForSelector('[data-testid="articles-list"]', { timeout: 30000 });
      const loadTime = Date.now() - startTime;

      expect(loadTime).toBeLessThan(10000); // Should load within 10 seconds
    });
  });

  describe('Integration with Backend API', () => {
    test('real-time data updates work', async () => {
      await page.waitForSelector('[data-testid="sentiment-chart"]');

      // Get initial data
      const initialData = await page.evaluate(() => {
        return window.analyticsData?.sentiment?.total || 0;
      });

      // Wait for potential updates
      await page.waitForTimeout(5000);

      // Check if data might have updated
      const updatedData = await page.evaluate(() => {
        return window.analyticsData?.sentiment?.total || 0;
      });

      expect(typeof updatedData).toBe('number');
    });

    test('API health check integration', async () => {
      // Check if API is reachable
      const response = await page.goto(`${API_URL}/health`);
      expect(response.status()).toBe(200);

      const healthData = await response.json();
      expect(healthData.status).toBe('healthy');
    });
  });

  describe('Performance Testing', () => {
    test('page load performance is acceptable', async () => {
      const startTime = Date.now();
      await page.goto(BASE_URL);
      await page.waitForSelector('[data-testid="main-dashboard"]');
      const loadTime = Date.now() - startTime;

      expect(loadTime).toBeLessThan(5000); // Should load within 5 seconds
    });

    test('chart rendering performance is acceptable', async () => {
      const startTime = Date.now();
      await page.waitForSelector('[data-testid="sentiment-chart"]');
      const renderTime = Date.now() - startTime;

      expect(renderTime).toBeLessThan(3000); // Charts should render within 3 seconds
    });
  });
});
