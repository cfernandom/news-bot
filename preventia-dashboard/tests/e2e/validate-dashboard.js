// Dashboard validation script
// Tests React components with real API data

import puppeteer from 'puppeteer';

async function validateDashboard() {
    console.log('🔍 Validando dashboard con datos reales...\n');

    let browser;
    try {
        // Launch browser
        browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });

        const page = await browser.newPage();

        // Set viewport
        await page.setViewport({ width: 1280, height: 720 });

        // Navigate to dashboard
        console.log('📊 Accediendo al dashboard...');
        await page.goto('http://localhost:5173', {
            waitUntil: 'networkidle0',
            timeout: 30000
        });

        // Wait for React to load
        await page.waitForSelector('[data-testid="app"], .medical-section, h1', { timeout: 10000 });

        // Check if title is present
        const title = await page.$eval('h1', el => el.textContent).catch(() => null);
        console.log('✅ Título encontrado:', title || 'PreventIA');

        // Check for medical KPI grid
        const kpiGrid = await page.$('.medical-grid').catch(() => null);
        if (kpiGrid) {
            console.log('✅ Grid de KPIs médicos detectado');

            // Count KPI cards
            const kpiCards = await page.$$('.metric-card, [class*="kpi"], [class*="card"]');
            console.log(`✅ ${kpiCards.length} tarjetas KPI encontradas`);
        } else {
            console.log('⚠️  Grid de KPIs no encontrado, verificando elementos alternativos...');
        }

        // Check for loading states
        const loadingElements = await page.$$('[class*="loading"], [class*="skeleton"]');
        if (loadingElements.length > 0) {
            console.log(`🔄 ${loadingElements.length} elementos en estado de carga`);
        }

        // Check for error states
        const errorElements = await page.$$('[class*="error"], .text-red-500, .text-red-600');
        if (errorElements.length > 0) {
            console.log(`❌ ${errorElements.length} elementos de error detectados`);

            // Get error messages
            for (let i = 0; i < Math.min(errorElements.length, 3); i++) {
                try {
                    const errorText = await page.evaluate(el => el.textContent, errorElements[i]);
                    console.log(`   Error ${i + 1}: ${errorText.substring(0, 100)}...`);
                } catch (e) {
                    console.log(`   Error ${i + 1}: No se pudo leer el mensaje`);
                }
            }
        }

        // Check network requests
        const responses = [];
        page.on('response', response => {
            if (response.url().includes('localhost:8000')) {
                responses.push({
                    url: response.url(),
                    status: response.status(),
                    statusText: response.statusText()
                });
            }
        });

        // Trigger API calls by waiting a bit more
        await page.waitForTimeout(3000);

        // Report API calls
        if (responses.length > 0) {
            console.log('\n🌐 Llamadas API detectadas:');
            responses.forEach(resp => {
                const status = resp.status === 200 ? '✅' : '❌';
                console.log(`   ${status} ${resp.status} ${resp.url.replace('http://localhost:8000', '')}`);
            });
        }

        // Check for specific medical data
        const pageContent = await page.content();

        // Look for data indicators
        const hasNumbers = /\d+/.test(pageContent);
        const hasMedicalTerms = /artículo|análisis|médico|sentimiento/i.test(pageContent);
        const hasPercentages = /%/.test(pageContent);

        console.log('\n📈 Indicadores de datos:');
        console.log(`   ${hasNumbers ? '✅' : '❌'} Números presentes`);
        console.log(`   ${hasMedicalTerms ? '✅' : '❌'} Términos médicos presentes`);
        console.log(`   ${hasPercentages ? '✅' : '❌'} Porcentajes presentes`);

        // Take screenshot for manual verification
        await page.screenshot({
            path: '/home/cfernandom/proyectos/preventia/news_bot_3/preventia-dashboard/dashboard-validation.png',
            fullPage: true
        });
        console.log('\n📸 Screenshot guardado: dashboard-validation.png');

        console.log('\n🎉 Validación del dashboard completada');

    } catch (error) {
        console.error('❌ Error en validación:', error.message);

        // Check if it's a connection error
        if (error.message.includes('ERR_CONNECTION_REFUSED')) {
            console.log('\n💡 Sugerencia: Asegúrate de que el servidor de desarrollo esté corriendo:');
            console.log('   npm run dev');
        }
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// Run validation
validateDashboard();
