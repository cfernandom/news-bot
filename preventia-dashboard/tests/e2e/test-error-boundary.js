// Test error boundary functionality
import puppeteer from 'puppeteer';

async function testErrorBoundary() {
    console.log('🛡️  Probando error boundary...\n');

    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    try {
        // Monitor console errors
        const consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
            }
        });

        // Test 1: Normal load (should not trigger error boundary)
        console.log('🔍 Test 1: Carga normal...');
        await page.goto('http://localhost:5173', { waitUntil: 'networkidle0' });

        const errorBoundaryUI = await page.$('[class*="error"], .bg-red-100, .text-red-600');
        const hasErrorUI = errorBoundaryUI !== null;

        console.log(`   Error boundary activado: ${hasErrorUI ? '❌ Sí (inesperado)' : '✅ No (correcto)'}`);

        // Test 2: Simulate API failure by blocking requests
        console.log('\n🔍 Test 2: Simulando fallo de API...');

        // Block API requests to simulate network failure
        await page.setRequestInterception(true);
        page.on('request', request => {
            if (request.url().includes('localhost:8000')) {
                request.abort();
            } else {
                request.continue();
            }
        });

        // Reload page to trigger API errors
        await page.reload({ waitUntil: 'networkidle0' });

        // Wait for error states to appear
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Check for error states in components
        const errorStates = await page.$$('[class*="error"], .text-red-500, .text-red-600');
        const retryButtons = await page.$$('button[class*="retry"], button:has-text("Reintentar")');

        console.log(`   Estados de error detectados: ${errorStates.length}`);
        console.log(`   Botones de reintento: ${retryButtons.length}`);

        // Check console errors
        if (consoleErrors.length > 0) {
            console.log(`   Errores en consola: ${consoleErrors.length}`);
            consoleErrors.slice(0, 2).forEach((error, i) => {
                console.log(`     ${i + 1}. ${error.substring(0, 80)}...`);
            });
        }

        // Test 3: Check error boundary recovery
        console.log('\n🔍 Test 3: Prueba de recuperación...');

        // Re-enable API requests
        await page.setRequestInterception(false);

        // Try to click retry button if available
        if (retryButtons.length > 0) {
            console.log('   Haciendo clic en botón de reintento...');
            await retryButtons[0].click();
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Check if error state is cleared
            const errorStatesAfterRetry = await page.$$('[class*="error"], .text-red-500');
            const recoveredSuccessfully = errorStatesAfterRetry.length < errorStates.length;

            console.log(`   Recuperación exitosa: ${recoveredSuccessfully ? '✅' : '❌'}`);
        }

        // Check for medical error boundary specific UI
        const medicalErrorUI = await page.$('[class*="medical-error"], .bg-blue-50');
        if (medicalErrorUI) {
            console.log('✅ UI de error médico encontrada');
        }

        console.log('\n🎉 Pruebas de error boundary completadas');

    } catch (error) {
        console.error('❌ Error en prueba:', error.message);
    } finally {
        await browser.close();
    }
}

testErrorBoundary();
