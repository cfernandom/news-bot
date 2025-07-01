// Test dual-mode functionality
import puppeteer from 'puppeteer';

async function testDualMode() {
    console.log('🔄 Probando funcionalidad dual-mode...\n');

    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    try {
        await page.goto('http://localhost:5173', { waitUntil: 'networkidle0' });

        // Look for mode toggle button
        const modeToggle = await page.$('[class*="toggle"], button[class*="mode"], [data-testid="mode-toggle"]');

        if (!modeToggle) {
            console.log('⚠️  Botón de cambio de modo no encontrado, buscando alternativas...');

            // Try to find any button that might be the mode toggle
            const buttons = await page.$$('button');
            console.log(`   ${buttons.length} botones encontrados en la página`);

            // Check for mode-related text
            for (let i = 0; i < Math.min(buttons.length, 5); i++) {
                const buttonText = await page.evaluate(el => el.textContent, buttons[i]);
                if (buttonText.toLowerCase().includes('mode') ||
                    buttonText.toLowerCase().includes('profesional') ||
                    buttonText.toLowerCase().includes('educativo')) {
                    console.log(`   Posible botón de modo: "${buttonText}"`);
                }
            }
        } else {
            console.log('✅ Botón de cambio de modo encontrado');

            // Test clicking the mode toggle
            const initialContent = await page.content();
            await modeToggle.click();

            // Wait for mode change
            await new Promise(resolve => setTimeout(resolve, 1000));

            const newContent = await page.content();
            const contentChanged = initialContent !== newContent;

            console.log(`   Cambio de contenido al hacer clic: ${contentChanged ? '✅' : '❌'}`);
        }

        // Check for dual-mode indicators in the DOM
        const professionalElements = await page.$$('[class*="professional"], [data-mode="professional"]');
        const educationalElements = await page.$$('[class*="educational"], [data-mode="educational"]');
        const adaptiveElements = await page.$$('[class*="adaptive"]');

        console.log('🎯 Elementos dual-mode detectados:');
        console.log(`   Elementos profesionales: ${professionalElements.length}`);
        console.log(`   Elementos educativos: ${educationalElements.length}`);
        console.log(`   Elementos adaptativos: ${adaptiveElements.length}`);

        // Check CSS classes for mode-specific styling
        const content = await page.content();
        const hasProfessionalCSS = /professional|academic/i.test(content);
        const hasEducationalCSS = /educational|student/i.test(content);
        const hasAdaptiveCSS = /adaptive/i.test(content);

        console.log('\n🎨 Clases CSS duales:');
        console.log(`   Estilos profesionales: ${hasProfessionalCSS ? '✅' : '❌'}`);
        console.log(`   Estilos educativos: ${hasEducationalCSS ? '✅' : '❌'}`);
        console.log(`   Estilos adaptativos: ${hasAdaptiveCSS ? '✅' : '❌'}`);

        // Check for context providers in React DevTools (if available)
        const contextProviders = await page.$$('[data-react-component*="Provider"], [data-react-component*="Context"]');
        if (contextProviders.length > 0) {
            console.log(`\n⚛️  ${contextProviders.length} proveedores de contexto React encontrados`);
        }

        console.log('\n🎉 Prueba dual-mode completada');

    } catch (error) {
        console.error('❌ Error en prueba dual-mode:', error.message);
    } finally {
        await browser.close();
    }
}

testDualMode();
