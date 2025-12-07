// CHART 1 : Répartition du portefeuille
var optionsPortfolio = {
    series: [52, 30, 18], // Actions, ETF, Crypto
    chart: {
        type: 'pie',
        height: 260
    },
    labels: ['Actions', 'ETF', 'Cryptomonnaies'],
    colors: ['#4F46E5', '#10B981', '#F59E0B'],
    legend: {
        position: 'bottom'
    }
};

var chartPortfolio = new ApexCharts(document.querySelector("#portfolioChart"), optionsPortfolio);
chartPortfolio.render();


// CHART 2 : Revenus vs Dépenses
var optionsIncomeExpense = {
    series: [{
        name: 'Revenus',
        data: [2300, 2400, 2450, 2500, 2550, 2600]
    }, {
        name: 'Dépenses',
        data: [1800, 1850, 1780, 1900, 2000, 1950]
    }],
    chart: {
        type: 'bar',
        height: 260
    },
    colors: ['#10B981', '#EF4444'],
    xaxis: {
        categories: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin']
    },
    plotOptions: {
        bar: {
            borderRadius: 5,
            horizontal: false
        }
    },
    dataLabels: {
        enabled: false
    }
};

var chartIncomeExpense = new ApexCharts(document.querySelector("#incomeExpenseChart"), optionsIncomeExpense);
chartIncomeExpense.render();