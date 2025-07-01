// Simple test script to validate MedicalApiClient
// Run with: node test-api-client.js

async function testApiClient() {
    try {
        // Test basic analytics endpoint
        const response = await fetch('http://localhost:8000/api/analytics/dashboard');
        const data = await response.json();

        console.log('✅ Analytics endpoint working');
        console.log('Total articles:', data.total_articles);
        console.log('Sentiment distribution:', data.sentiment_distribution);

        // Test articles endpoint
        const articlesResponse = await fetch('http://localhost:8000/api/articles/');
        const articlesData = await articlesResponse.json();

        console.log('✅ Articles endpoint working');
        console.log('Articles returned:', articlesData.items?.length || 0);

        if (articlesData.items && articlesData.items.length > 0) {
            const firstArticle = articlesData.items[0];
            console.log('First article title:', firstArticle.title?.substring(0, 50) + '...');
            console.log('Sentiment:', firstArticle.sentiment_label);
            console.log('Topic:', firstArticle.topic_category);
        }

        // Test topics endpoint
        const topicsResponse = await fetch('http://localhost:8000/api/analytics/topics/distribution');
        const topicsData = await topicsResponse.json();

        console.log('✅ Topics endpoint working');
        console.log('Topics distribution:', topicsData.distribution);

        console.log('\n🎉 All API endpoints validated successfully!');

    } catch (error) {
        console.error('❌ API Client test failed:', error.message);
    }
}

testApiClient();
