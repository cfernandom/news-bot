// Simple dashboard validation
import puppeteer from 'puppeteer';

async function quickValidation() {
    console.log('🔍 Validación rápida del dashboard...\n');

    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    try {
        // Track API responses
        const apiCalls = [];
        page.on('response', response => {
            if (response.url().includes('localhost:8000')) {
                apiCalls.push({
                    url: response.url().replace('http://localhost:8000', ''),
                    status: response.status()
                });
            }
        });

        await page.goto('http://localhost:5173', { waitUntil: 'networkidle0' });

        // Check basic elements
        const title = await page.$eval('h1', el => el.textContent);
        const hasKPIGrid = await page.$('.medical-grid') !== null;
        const kpiCount = (await page.$$('.metric-card, [class*="card"]')).length;

        console.log('✅ Elementos básicos:');
        console.log(`   Título: ${title}`);
        console.log(`   Grid KPI: ${hasKPIGrid ? '✅ Presente' : '❌ Ausente'}`);
        console.log(`   Tarjetas KPI: ${kpiCount}`);

        // Wait for API calls
        await new Promise(resolve => setTimeout(resolve, 3000));

        console.log('\n🌐 Llamadas API:');
        if (apiCalls.length === 0) {
            console.log('   ⚠️  Ninguna llamada API detectada');
        } else {
            apiCalls.forEach(call => {
                const status = call.status === 200 ? '✅' : '❌';
                console.log(`   ${status} ${call.status} ${call.url}`);
            });
        }

        // Check for actual data values in the page
        const content = await page.content();
        const hasNumbers = /\b\d{1,3}\b/.test(content);
        const hasPercentages = /\d+(\.\d+)?%/.test(content);
        const hasMedicalTerms = /artículo|análisis|sentimiento|positivo|negativo/i.test(content);

        console.log('\n📊 Datos mostrados:');
        console.log(`   Números: ${hasNumbers ? '✅' : '❌'}`);
        console.log(`   Porcentajes: ${hasPercentages ? '✅' : '❌'}`);
        console.log(`   Términos médicos: ${hasMedicalTerms ? '✅' : '❌'}`);

        console.log('\n🎉 Validación completada exitosamente');

    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await browser.close();
    }
}

quickValidation();
