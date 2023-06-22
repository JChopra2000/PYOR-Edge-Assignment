"use client";
import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import * as echarts from 'echarts';

const Page = () => {
  const [chartInstance, setChartInstance] = useState(null);

  const renderChart = async () => {
    if (!chartInstance) {
      const response = await fetch('http://localhost:5000/fetch_data'); // Replace '/api/data' with the actual endpoint URL
      const data = await response.json();
  
      const chartDom = document.getElementById('main');
      const myChart = echarts.init(chartDom);
      // const xAxisData = data.result.rows.map((row: { day: any; }) => row.day);
      const xAxisData = data.result.rows.map((row: { day: string | number | Date; }) => {
        const date = new Date(row.day);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
      });
      const seriesData = data.result.rows.map((row: { average_transactions_per_block: any; }) => row.average_transactions_per_block);
      console.log(xAxisData)
      const option = {
        xAxis: {
          type: 'category',
          data: xAxisData // Assuming the data from the endpoint has an 'xAxisData' property
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Data', // Legend label for the series
            data: seriesData,
            type: 'line'
          }
        ],
        legend: {
          data: ['Data'] // Array of legend labels to display
        }
      };
      option && myChart.setOption(option);
      setChartInstance(myChart);
    }
  };
  

  useEffect(() => {
    const getClient = () => import('next/client').then((mod) => mod);
    getClient().then((client) => {
      const echarts = client.echarts;
      renderChart();
    });
  }, []);

  return (
    <div>
      <div id="main" style={{ width: '1200px', height: '800px' }}></div>
    </div>
  );
};

export default Page;
