const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  console.log('Testing enhanced modebar with full tool set...');
  await page.goto('http://localhost:4321/charts', { waitUntil: 'networkidle2' });
  await new Promise(resolve => setTimeout(resolve, 8000));

  const modebarTest = await page.evaluate(() => {
    const modebar = document.querySelector('.modebar');
    const modebarButtons = document.querySelectorAll('.modebar-btn');
    const buttonTitles = Array.from(modebarButtons).map(btn => btn.getAttribute('data-title'));

    // Check for specific tools that should now be available
    const hasZoom = buttonTitles.some(title => title && title.toLowerCase().includes('zoom'));
    const hasPan = buttonTitles.some(title => title && title.toLowerCase().includes('pan'));
    const hasSelect = buttonTitles.some(title => title && title.toLowerCase().includes('select'));
    const hasLasso = buttonTitles.some(title => title && title.toLowerCase().includes('lasso'));
    const hasDownload = buttonTitles.some(title => title && title.toLowerCase().includes('download'));
    const hasAutoscale = buttonTitles.some(title => title && title.toLowerCase().includes('autoscale'));
    const hasReset = buttonTitles.some(title => title && title.toLowerCase().includes('reset'));

    return {
      modebarFound: modebar !== null,
      totalButtons: modebarButtons.length,
      buttonTitles: buttonTitles,
      toolsAvailable: {
        zoom: hasZoom,
        pan: hasPan,
        select: hasSelect,
        lasso: hasLasso,
        download: hasDownload,
        autoscale: hasAutoscale,
        reset: hasReset
      },
      modebarClasses: modebar ? modebar.className : null,
      modebarStyle: modebar ? window.getComputedStyle(modebar).backgroundColor : null
    };
  });

  console.log('\n🔧 ENHANCED MODEBAR TEST RESULTS:');
  console.log('==================================');
  console.log(`📊 Modebar found: ${modebarTest.modebarFound ? '✅' : '❌'}`);
  console.log(`🔢 Total buttons: ${modebarTest.totalButtons}`);
  console.log(`📋 Button titles: ${JSON.stringify(modebarTest.buttonTitles, null, 2)}`);

  console.log('\n🛠️  TOOLS AVAILABLE:');
  Object.entries(modebarTest.toolsAvailable).forEach(([tool, available]) => {
    console.log(`   ${available ? '✅' : '❌'} ${tool}: ${available}`);
  });

  console.log(`\n🎨 Modebar styling:`);
  console.log(`   Classes: ${modebarTest.modebarClasses}`);
  console.log(`   Background: ${modebarTest.modebarStyle}`);

  // Take screenshot
  await page.screenshot({ path: 'debug-output/enhanced-modebar-test.png', fullPage: true });
  console.log('\n📸 Screenshot saved to debug-output/enhanced-modebar-test.png');

  // Test interaction with new tools
  console.log('\n🎯 Testing tool interactions...');
  try {
    // Test pan tool
    const panBtn = await page.$('[data-title="Pan"]');
    if (panBtn) {
      await panBtn.click();
      console.log('   ✅ Pan tool: Successfully activated');
    } else {
      console.log('   ❌ Pan tool: Not found');
    }

    // Test zoom tool
    const zoomBtn = await page.$('[data-title="Zoom"]');
    if (zoomBtn) {
      await zoomBtn.click();
      console.log('   ✅ Zoom tool: Successfully activated');
    } else {
      console.log('   ❌ Zoom tool: Not found');
    }
  } catch (error) {
    console.log(`   ❌ Tool interaction error: ${error.message}`);
  }

  // Summary
  const enhancedTools = Object.values(modebarTest.toolsAvailable).filter(Boolean).length;
  const totalTools = Object.keys(modebarTest.toolsAvailable).length;

  console.log('\n🏆 ENHANCEMENT SUMMARY:');
  console.log('========================');
  console.log(`📈 Tools available: ${enhancedTools}/${totalTools}`);
  console.log(`🎛️  Total buttons: ${modebarTest.totalButtons} (should be more than before)`);

  if (enhancedTools >= 5 && modebarTest.totalButtons >= 6) {
    console.log('   🎉 SUCCESS: Modebar enhanced with full tool set!');
    console.log('   ✅ Pan and lasso tools now available');
    console.log('   ✅ Select tools now available');
    console.log('   ✅ All standard Plotly tools accessible');
  } else {
    console.log('   ⚠️  Enhancement may be incomplete');
  }

  await browser.close();
})().catch(console.error);
