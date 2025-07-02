// SentimentChart Integration Validation - Day 1 Sprint Week 2
// Validates that the SentimentChart component loads and displays real sentiment data

import puppeteer from 'puppeteer';

async function validateSentimentChart() {
  console.log('🔍 INICIANDO VALIDACIÓN SENTIMENTCHART - DAY 1 SPRINT');

  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: { width: 1280, height: 720 }
  });

  try {
    const page = await browser.newPage();

    console.log('📊 1. Navegando al dashboard...');
    await page.goto('http://localhost:5174', { waitUntil: 'networkidle0' });

    // Verificar que el dashboard base carga
    console.log('🏥 2. Verificando carga del dashboard base...');
    await page.waitForSelector('h1', { timeout: 5000 });
    const title = await page.$eval('h1', el => el.textContent);
    console.log(`   ✅ Título dashboard: "${title}"`);

    // Verificar la nueva sección de visualizaciones
    console.log('📈 3. Verificando sección de visualizaciones médicas...');
    const visualizationSection = await page.waitForSelector('h2:contains("📊 Análisis Visual de Datos Médicos")', { timeout: 10000 }).catch(() => null);

    if (!visualizationSection) {
      // Buscar de manera alternativa
      const sections = await page.$$eval('h2', elements =>
        elements.map(el => el.textContent).filter(text => text.includes('Análisis Visual'))
      );

      if (sections.length > 0) {
        console.log(`   ✅ Sección encontrada: "${sections[0]}"`);
      } else {
        console.log('   ⚠️  Sección de visualizaciones no encontrada, buscando componentes...');
      }
    } else {
      console.log('   ✅ Sección de visualizaciones médicas encontrada');
    }

    // Verificar que existe el componente SentimentChart
    console.log('🎭 4. Verificando componente SentimentChart...');

    // Buscar elementos específicos del SentimentChart
    const chartElements = await page.evaluate(() => {
      const elements = {
        charts: document.querySelectorAll('svg').length,
        chartContainers: document.querySelectorAll('[class*="recharts"], [class*="chart"]').length,
        sentimentElements: Array.from(document.querySelectorAll('*')).filter(el =>
          el.textContent && (
            el.textContent.includes('Sentimiento') ||
            el.textContent.includes('Positivo') ||
            el.textContent.includes('Negativo') ||
            el.textContent.includes('positivas') ||
            el.textContent.includes('negativas')
          )
        ).length,
        loadingSpinners: document.querySelectorAll('[class*="animate-pulse"], [class*="loading"]').length
      };
      return elements;
    });

    console.log(`   📊 Charts SVG detectados: ${chartElements.charts}`);
    console.log(`   🎯 Contenedores chart detectados: ${chartElements.chartContainers}`);
    console.log(`   😊 Elementos sentiment detectados: ${chartElements.sentimentElements}`);
    console.log(`   ⏳ Loading states detectados: ${chartElements.loadingSpinners}`);

    // Verificar datos API
    console.log('🔗 5. Verificando integración API...');

    // Interceptar llamadas de red para verificar que se llama al API
    const apiCalls = [];
    page.on('response', response => {
      if (response.url().includes('localhost:8000')) {
        apiCalls.push({
          url: response.url(),
          status: response.status(),
          timestamp: new Date().toISOString()
        });
      }
    });

    // Esperar un poco para que las llamadas API se completen
    await page.waitForTimeout(3000);

    console.log(`   🌐 Llamadas API detectadas: ${apiCalls.length}`);
    apiCalls.forEach(call => {
      console.log(`     - ${call.url} (${call.status})`);
    });

    // Verificar modo dual-mode
    console.log('🔄 6. Verificando sistema dual-mode...');
    const modeToggle = await page.$('[class*="mode"], button:contains("Modo")').catch(() => null);
    if (modeToggle) {
      console.log('   ✅ ModeToggle encontrado');

      // Intentar alternar modo
      await modeToggle.click();
      await page.waitForTimeout(1000);

      const modeElements = await page.evaluate(() => {
        const educational = document.querySelectorAll('[class*="educational"]').length;
        const professional = document.querySelectorAll('[class*="professional"]').length;
        const adaptive = document.querySelectorAll('[class*="adaptive"]').length;
        return { educational, professional, adaptive };
      });

      console.log(`   🎓 Elementos educativos: ${modeElements.educational}`);
      console.log(`   🏥 Elementos profesionales: ${modeElements.professional}`);
      console.log(`   🔄 Elementos adaptativos: ${modeElements.adaptive}`);
    } else {
      console.log('   ⚠️  ModeToggle no encontrado');
    }

    // Screenshot para evidencia
    console.log('📸 7. Capturando screenshot del dashboard...');
    await page.screenshot({
      path: 'tests/e2e/sentiment-chart-validation.png',
      fullPage: true
    });

    // Resultados finales
    console.log('\n🎯 RESULTADOS VALIDACIÓN SENTIMENTCHART:');
    console.log('=====================================');

    const results = {
      dashboardLoaded: title?.includes('PreventIA') || false,
      hasCharts: chartElements.charts > 0,
      hasSentimentContent: chartElements.sentimentElements > 0,
      hasApiIntegration: apiCalls.length > 0,
      hasSuccessfulApiCalls: apiCalls.filter(call => call.status === 200).length > 0
    };

    Object.entries(results).forEach(([key, value]) => {
      const status = value ? '✅' : '❌';
      const description = {
        dashboardLoaded: 'Dashboard base cargado',
        hasCharts: 'Componentes chart presentes',
        hasSentimentContent: 'Contenido sentiment presente',
        hasApiIntegration: 'Integración API activa',
        hasSuccessfulApiCalls: 'Llamadas API exitosas'
      }[key];
      console.log(`${status} ${description}: ${value}`);
    });

    const successRate = Object.values(results).filter(Boolean).length / Object.values(results).length;
    console.log(`\n📊 TASA DE ÉXITO: ${(successRate * 100).toFixed(1)}%`);

    if (successRate >= 0.8) {
      console.log('🚀 SENTIMENTCHART INTEGRATION: EXITOSA');
    } else if (successRate >= 0.6) {
      console.log('🟡 SENTIMENTCHART INTEGRATION: PARCIAL - Revisar issues');
    } else {
      console.log('🔴 SENTIMENTCHART INTEGRATION: FALLIDA - Requiere corrección');
    }

    return results;

  } catch (error) {
    console.error('❌ Error durante validación:', error.message);
    return { error: error.message };
  } finally {
    await browser.close();
  }
}

// Ejecutar validación si se llama directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  validateSentimentChart()
    .then(results => {
      console.log('\n🏁 Validación completada');
      process.exit(results.error ? 1 : 0);
    })
    .catch(error => {
      console.error('💥 Error fatal:', error);
      process.exit(1);
    });
}

export { validateSentimentChart };
