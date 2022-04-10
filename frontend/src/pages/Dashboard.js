import React, { useRef, useState, useEffect } from 'react';
import classes from '../styles';
import { useNavigate } from 'react-router-dom';
import DashboardService from '../services/dashboard.service';
import AuthService from '../services/auth.service';

import CanvasJSReact from '../assets/canvasjs.react';
import { checkAuth } from '../utils/auth';
const CanvasJSChart = CanvasJSReact.CanvasJSChart;

const MAX_LENGTH = 1 * 60 * 4;

const Dashboard = () => {
    const navigate = useNavigate();
    const logout = () => {
        AuthService.logout()
        .then(() => {
            navigate("/");
        });
    }
    const [showChart, setShowChart] = useState(false);
    let dataPoints1 = [], dataPoints2 = [];

    useEffect(() => {
        checkAuth().then((isAuthenticated) =>{
            if(!isAuthenticated){
                navigate("/");
            }
        }); 
    }, [navigate]);

    useEffect(() => {
        if (showChart) {
            const interval = setInterval(refresh, 1000);
            return () => clearInterval(interval);
        }
    }, [showChart]);

    let chart = useRef();

    let options = {
        theme: "light2",
        animationEnabled: true,
        title: {
            text: "My Chart"
        },
        subtitles: [{
            text: "Time series"
        }],
        axisX: {
            valueFormatString: "HH:mm:ss",
            interval: 20,
            intervalType: "second"
        },
        axisY: {
            includeZero: true,
            interval: 10,
        },
        toolTip: {
            shared: true
        },
        data: [
            {
                type: "line",
                name: "Line1",
                showInLegend: true,
                xValueFormatString: "HH:mm:ss",
                yValueFormatString: "#,##0.##",
                dataPoints: [
                ]
            },
            {
                type: "line",
                name: "Line2",
                showInLegend: true,
                xValueFormatString: "HH:mm:ss",
                yValueFormatString: "#,##0.##",
                dataPoints: [
                ]
            }
        ]
    };

    const refresh = () => {
        DashboardService.getData().then((response) => {
            let now = new Date();
            dataPoints1.push({ x: now, y: response.data[0] });
            dataPoints1.push({ x: new Date(now.getTime() + 250), y: response.data[1] });
            dataPoints1.push({ x: new Date(now.getTime() + 500), y: response.data[2] });
            dataPoints1.push({ x: new Date(now.getTime() + 750), y: response.data[3] });

            dataPoints2.push({ x: now, y: response.data[4] });
            dataPoints2.push({ x: new Date(now.getTime() + 250), y: response.data[5] });
            dataPoints2.push({ x: new Date(now.getTime() + 500), y: response.data[6] });
            dataPoints2.push({ x: new Date(now.getTime() + 750), y: response.data[7] });

            if (dataPoints1.length > MAX_LENGTH) {
                dataPoints1.splice(0, dataPoints1.length - MAX_LENGTH);
            }

            if (dataPoints2.length > MAX_LENGTH) {
                dataPoints2.splice(0, dataPoints2.length - MAX_LENGTH);
            }

            chart.options.data[0].dataPoints = dataPoints1;
            chart.options.data[1].dataPoints = dataPoints2;
            chart.render();
        });        
    };

    return (
        <div>
            <nav className={classes.nav}>
                <ul className={classes.ul}>
                    <li className={classes.li}>
                        <button className={classes.navBtn} onClick={() => setShowChart(true)}>
                            Chart
                        </button>
                    </li>
                    <li className={classes.li}>
                        <button className={classes.navBtn} onClick={() => logout()}>
                            Log out
                        </button>
                    </li>
                </ul>
            </nav>
            {
                showChart &&
                <div>
                    <CanvasJSChart options={options} onRef={ref => chart = ref} />
                </div>
            }
        </div>
    );
}

export default Dashboard;
