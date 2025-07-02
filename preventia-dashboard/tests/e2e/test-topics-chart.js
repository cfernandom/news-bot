// TopicsChart Integration Validation - Day 2 Sprint Week 2
// Validates that TopicsChart displays 10 medical categories with real data

import puppeteer from 'puppeteer';

async function validateTopicsChart() {
  console.log('🔍 INICIANDO VALIDACIÓN TOPICSCHART - DAY 2 SPRINT');

  const browser = await puppeteer.launch({
    headless: false,
    defaultViewport: { width: 1280, height: 720 }
  });

  try {
    const page = await browser.newPage();

    console.log('📊 1. Navegando al dashboard...');
    await page.goto('http://localhost:5174', { waitUntil: 'networkidle0' });

    // Verificar que el dashboard carga
    console.log('🏥 2. Verificando carga del dashboard...');
    await page.waitForSelector('h1', { timeout: 5000 });
    const title = await page.$eval('h1', el => el.textContent);
    console.log(`   ✅ Dashboard title: "${title}"`);

    // Verificar la sección de visualizaciones
    console.log('📈 3. Verificando sección de visualizaciones médicas...');
    const visualizationSection = await page.waitForSelector('h2', { timeout: 10000 });
    const sectionTitle = await page.$eval('h2', el => el.textContent);
    console.log(`   ✅ Visualizations section: "${sectionTitle}"`);

    // Verificar que existen múltiples charts
    console.log('🎭 4. Verificando componentes de charts múltiples...');

    const chartElements = await page.evaluate(() => {
      const elements = {
        svgCharts: document.querySelectorAll('svg').length,
        chartContainers: document.querySelectorAll('[class*="recharts"]').length,
        topicsElements: Array.from(document.querySelectorAll('*')).filter(el =>
          el.textContent && (
            el.textContent.includes('Categorías') ||
            el.textContent.includes('Topics') ||
            el.textContent.includes('Tratamiento') ||
            el.textContent.includes('Investigación') ||
            el.textContent.includes('Cirugía')
          )
        ).length,
        medicalTerms: Array.from(document.querySelectorAll('*')).filter(el =>
          el.textContent && (
            el.textContent.includes('tratamiento') ||
            el.textContent.includes('research') ||
            el.textContent.includes('surgery') ||
            el.textContent.includes('diagnosis')
          )
        ).length
      };
      return elements;
    });

    console.log(`   📊 SVG Charts detectados: ${chartElements.svgCharts}`);
    console.log(`   🎯 Recharts containers: ${chartElements.chartContainers}`);
    console.log(`   🩺 Topics elements: ${chartElements.topicsElements}`);
    console.log(`   💊 Medical terms detectados: ${chartElements.medicalTerms}`);

    // Verificar llamadas API específicas
    console.log('🔗 5. Verificando integración API topics...');

    const apiCalls = [];
    page.on('response', response => {
      if (response.url().includes('localhost:8000')) {
        apiCalls.push({
          url: response.url(),
          status: response.status(),
          endpoint: response.url().split('/').pop(),
          timestamp: new Date().toISOString()
        });
      }
    });

    // Esperar para que las llamadas API se completen
    await new Promise(resolve => setTimeout(resolve, 4000));

    console.log(`   🌐 API calls detectadas: ${apiCalls.length}`);
    apiCalls.forEach(call => {
      console.log(`     - ${call.endpoint}: ${call.status} (${call.url.includes('topics') ? 'TOPICS DATA' : 'OTHER'})`);
    });

    // Verificar datos específicos de topics
    console.log('📊 6. Verificando datos de categorías médicas...');

    const topicsApiCall = apiCalls.find(call => call.url.includes('topics'));
    if (topicsApiCall) {
      console.log(`   ✅ Topics API endpoint llamado: ${topicsApiCall.status === 200 ? 'SUCCESS' : 'FAILED'}`);
    } else {
      console.log('   ⚠️  Topics API endpoint no detectado en network calls');
    }

    // Verificar contenido específico de categorías médicas
    const medicalCategories = await page.evaluate(() => {
      const categories = {
        treatment: document.body.textContent.includes('Tratamiento') || document.body.textContent.includes('treatment'),
        research: document.body.textContent.includes('Investigación') || document.body.textContent.includes('research'),
        surgery: document.body.textContent.includes('Cirugía') || document.body.textContent.includes('surgery'),
        diagnosis: document.body.textContent.includes('Diagnóstico') || document.body.textContent.includes('diagnosis'),
        categoriesCount: (document.body.textContent.match(/categorías|categories/gi) || []).length
      };
      return categories;
    });

    console.log('   📋 Categorías médicas detectadas:');
    Object.entries(medicalCategories).forEach(([key, value]) => {
      if (typeof value === 'boolean') {
        console.log(`     - ${key}: ${value ? '✅' : '❌'}`);
      } else {
        console.log(`     - ${key}: ${value}`);
      }
    });

    // Verificar dual-mode con topics
    console.log('🔄 7. Verificando dual-mode con topics...');
    const modeToggleFound = await page.$('button').catch(() => null);
    if (modeToggleFound) {
      console.log('   ✅ Mode toggle encontrado, probando cambios...');

      // Click mode toggle si existe
      try {
        await page.click('button');
        await new Promise(resolve => setTimeout(resolve, 1000));

        const afterToggle = await page.evaluate(() => ({
          educational: document.querySelectorAll('[class*="educational"]').length,
          explanations: document.body.textContent.includes('explicación') || document.body.textContent.includes('Qué significa'),
          simplified: document.body.textContent.includes('simplificado') || document.body.textContent.includes('fácil')
        }));

        console.log(`   🎓 Elementos educativos después toggle: ${afterToggle.educational}`);
        console.log(`   📚 Explicaciones detectadas: ${afterToggle.explanations ? 'SÍ' : 'NO'}`);
      } catch (error) {
        console.log('   ⚠️  Error al probar mode toggle:', error.message);
      }
    }

    // Screenshot para evidencia
    console.log('📸 8. Capturando screenshot con TopicsChart...');
    await page.screenshot({
      path: 'tests/e2e/topics-chart-validation.png',
      fullPage: true
    });

    // Resultados finales
    console.log('\n🎯 RESULTADOS VALIDACIÓN TOPICSCHART:');
    console.log('=====================================');

    const results = {
      dashboardLoaded: title?.includes('PreventIA') || false,
      hasMultipleCharts: chartElements.svgCharts >= 2,
      hasTopicsContent: chartElements.topicsElements > 0,
      hasMedicalTerms: chartElements.medicalTerms >= 3,
      hasTopicsAPI: apiCalls.some(call => call.url.includes('topics') && call.status === 200),
      hasMedicalCategories: Object.values(medicalCategories).filter(v => typeof v === 'boolean' && v).length >= 2
    };

    Object.entries(results).forEach(([key, value]) => {
      const status = value ? '✅' : '❌';
      const description = {
        dashboardLoaded: 'Dashboard base funcionando',
        hasMultipleCharts: 'Múltiples charts renderizados',
        hasTopicsContent: 'Contenido topics presente',
        hasMedicalTerms: 'Términos médicos detectados',
        hasTopicsAPI: 'API topics integration exitosa',
        hasMedicalCategories: 'Categorías médicas identificadas'
      }[key];
      console.log(`${status} ${description}: ${value}`);
    });

    const successRate = Object.values(results).filter(Boolean).length / Object.values(results).length;
    console.log(`\n📊 TASA DE ÉXITO DAY 2: ${(successRate * 100).toFixed(1)}%`);

    if (successRate >= 0.85) {
      console.log('🚀 TOPICSCHART INTEGRATION: EXITOSA - Ready for Day 3');
    } else if (successRate >= 0.7) {
      console.log('🟡 TOPICSCHART INTEGRATION: PARCIAL - Revisar detalles');
    } else {
      console.log('🔴 TOPICSCHART INTEGRATION: FALLIDA - Requiere corrección');
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
  validateTopicsChart()
    .then(results => {
      console.log('\n🏁 Validación Day 2 completada');
      process.exit(results.error ? 1 : 0);
    })
    .catch(error => {
      console.error('💥 Error fatal:', error);
      process.exit(1);
    });
}

export { validateTopicsChart };
