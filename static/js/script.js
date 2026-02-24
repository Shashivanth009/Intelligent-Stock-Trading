document.addEventListener('DOMContentLoaded', () => {
    const trainBtn = document.getElementById('trainBtn');
    const epochsInput = document.getElementById('epochs');
    const windowInput = document.getElementById('window');
    const balanceInput = document.getElementById('balance');
    const fileInput = document.getElementById('fileInput');
    const dropArea = document.getElementById('drop-area');
    const fileNameDisplay = document.getElementById('fileName');

    // Controls
    const btnLine = document.getElementById('btnLine');
    const btnCandle = document.getElementById('btnCandle');
    const checkPrediction = document.getElementById('checkPrediction');
    const checkSMA = document.getElementById('checkSMA');
    const checkEMA = document.getElementById('checkEMA');

    let uploadedFilePath = null;
    let currentData = null; // Store data for re-rendering
    let chartType = 'line'; // 'line' or 'candle'

    // --- File Upload Logic ---
    dropArea.addEventListener('click', () => fileInput.click());

    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileUpload(fileInput.files[0]);
        }
    });

    function handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        fileNameDisplay.textContent = "Uploading...";

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    fileNameDisplay.textContent = "Upload Failed";
                } else {
                    uploadedFilePath = data.filepath;
                    fileNameDisplay.textContent = data.filename;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                fileNameDisplay.textContent = "Upload Failed";
            });
    }

    // --- Training Logic ---
    trainBtn.addEventListener('click', async () => {
        trainBtn.disabled = true;
        trainBtn.textContent = 'Running Simulation...';

        const payload = {
            filepath: uploadedFilePath,
            epochs: epochsInput.value,
            window_size: windowInput.value,
            initial_balance: balanceInput.value
        };

        try {
            const response = await fetch('/api/train', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                currentData = data;
                updateMetrics(data);
                renderPlotlyChart();
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during simulation.');
        } finally {
            trainBtn.disabled = false;
            trainBtn.textContent = 'Start Simulation';
        }
    });

    function updateMetrics(data) {
        const currency = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR'
        });

        document.getElementById('netProfit').textContent = currency.format(data.net_profit);
        document.getElementById('finalValue').textContent = currency.format(data.final_value);
        document.getElementById('roi').textContent = data.roi.toFixed(2) + '%';
        document.getElementById('totalTrades').textContent = data.total_trades;
        document.getElementById('sharpeRatio').textContent = data.sharpe_ratio.toFixed(4);
        document.getElementById('maxDrawdown').textContent = data.max_drawdown.toFixed(2) + '%';
    }

    // --- Charting Logic (Plotly) ---
    function renderPlotlyChart() {
        if (!currentData) return;

        const traces = [];
        const dates = currentData.dates; // Expecting ISO date strings from backend

        // 1. Base Trace (Candle or Line)
        if (chartType === 'candle') {
            const ohlc = currentData.ohlc;
            traces.push({
                x: dates,
                close: ohlc.close,
                decreasing: { line: { color: '#ff0055' } },
                high: ohlc.high,
                increasing: { line: { color: '#00f2ff' } },
                line: { color: 'rgba(31,119,180,1)' },
                low: ohlc.low,
                open: ohlc.open,
                type: 'candlestick',
                xaxis: 'x',
                yaxis: 'y',
                name: 'OHLC'
            });
        } else {
            traces.push({
                x: dates,
                y: currentData.actual_prices,
                type: 'scatter',
                mode: 'lines',
                name: 'Actual Price',
                line: { color: 'rgba(255, 255, 255, 0.8)', width: 2 }
            });
        }

        // 2. Prediction Overlay
        if (checkPrediction.checked) {
            traces.push({
                x: dates,
                y: currentData.predicted_prices,
                type: 'scatter',
                mode: 'lines',
                name: 'Predicted',
                line: { color: '#00f2ff', width: 2 }, // Neon Cyan
                fill: 'tozeroy', // Optional: fill under
                fillcolor: 'rgba(0, 242, 255, 0.05)'
            });
        }

        // 3. Indicators
        if (checkSMA.checked && currentData.indicators.sma) {
            traces.push({
                x: dates,
                y: currentData.indicators.sma,
                type: 'scatter',
                mode: 'lines',
                name: 'SMA (5)',
                line: { color: '#ffaa00', width: 1.5, dash: 'dot' }
            });
        }

        if (checkEMA.checked && currentData.indicators.ema) {
            traces.push({
                x: dates,
                y: currentData.indicators.ema,
                type: 'scatter',
                mode: 'lines',
                name: 'EMA (5)',
                line: { color: '#ff0055', width: 1.5 }
            });
        }

        const layout = {
            plot_bgcolor: 'rgba(0,0,0,0)',
            paper_bgcolor: 'rgba(0,0,0,0)',
            font: {
                color: '#a0a0a0',
                family: 'Outfit, sans-serif'
            },
            hoverlabel: {
                bgcolor: '#0f0c29',
                bordercolor: '#00f2ff',
                font: { color: '#ffffff', family: 'Outfit, sans-serif' }
            },
            xaxis: {
                type: 'date',
                rangeslider: { visible: false },
                gridcolor: 'rgba(255,255,255,0.1)',
                zerolinecolor: 'rgba(255,255,255,0.1)',
                showspikes: true,
                spikethickness: 1,
                spikedash: 'dot',
                spikecolor: '#00f2ff',
                spikemode: 'across'
            },
            yaxis: {
                gridcolor: 'rgba(255,255,255,0.1)',
                zerolinecolor: 'rgba(255,255,255,0.1)',
                fixedrange: false
            },
            margin: { l: 50, r: 20, t: 40, b: 40 },
            showlegend: true,
            legend: {
                orientation: 'h',
                y: 1.1,
                x: 0.5,
                xanchor: 'center',
                font: { color: '#fff' }
            },
            dragmode: 'zoom',
            hovermode: 'x unified'
        };

        const config = {
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['lasso2d', 'select2d'],
            displaylogo: false,
            scrollZoom: true
        };

        Plotly.newPlot('stockChart', traces, layout, config);
    }

    // --- Event Listeners for Controls ---
    btnLine.addEventListener('click', () => {
        chartType = 'line';
        btnLine.classList.add('active');
        btnCandle.classList.remove('active');
        renderPlotlyChart();
    });

    btnCandle.addEventListener('click', () => {
        chartType = 'candle';
        btnCandle.classList.add('active');
        btnLine.classList.remove('active');
        renderPlotlyChart();
    });

    checkPrediction.addEventListener('change', renderPlotlyChart);
    checkSMA.addEventListener('change', renderPlotlyChart);
    checkEMA.addEventListener('change', renderPlotlyChart);
});
