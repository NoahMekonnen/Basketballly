const form = $('form')
if (form[0].id == "raw") {
    const inputs = $('input')
    const canvas = document.querySelector('canvas')
   
    form.on('submit', async function (e) {
        e.preventDefault()
        $('.form-Container').remove()
        const name = inputs[1].value
        const teamName = inputs[2].value
        const season = inputs[3].value
        let teamId;

        const teams = await getTeams();
        for (let team of teams) {
            if (team.name == teamName) {
                teamId = team.id
            }
        }
        const players = await getPlayersRequest(teamId, season)

        for (let player of players) {
            if (player.firstname + " " + player.lastname == inputs[1].value) {
                const id = player.id
                const player_games = await getPlayerStatistic(id, season)
                let free_throw_attempted = 0
                let free_throw_made = 0
                let three_point_attempted = 0
                let three_point_made = 0
                let assists = 0
                let turnovers = 0
                let offRebounds = 0
                let defRebounds = 0
                for (let game of player_games) {
                    free_throw_attempted += game.fta
                    free_throw_made += game.ftm
                    three_point_attempted += game.tpa
                    three_point_made += game.tpm
                    assists += game.assists
                    turnovers += game.turnovers
                    offRebounds += game.offReb
                    defRebounds += game.defReb
                }

                // let avg_points = total_points/player_games.length
                const total_rebounds = offRebounds + defRebounds
                const xValues = ["Free Throws Made vs. Attempted", "Three Point Made vs. Attempted",
                    "Assists-Turnovers", "Offensive vs total Rebounds"]
                const yValues1 = [free_throw_made, three_point_made, assists, offRebounds]
                const yValues2 = [three_point_attempted, three_point_attempted, turnovers, total_rebounds]

                // {
                //     label: 'Dataset 1',
                //     data: Utils.numbers(NUMBER_CFG),
                //     backgroundColor: Utils.CHART_COLORS.red,
                //   }

                const barChart = new Chart(canvas, {
                    type: "bar",
                    data: {
                        labels: xValues,
                        datasets: [{
                            label: 'Relevant Stats',
                            backgroundColor: "green",
                            data: yValues1
                        },
                        {
                            label: 'Total Stats',
                            backgroundColor: "red",
                            data: yValues2
                        }]
                    }, options: {
                        plugins: {
                            title: {
                                display: true,
                                text: 'Stacked Bar chart for pollution status',
                                color: 'black'
                            },
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }],
                            x: {
                                stacked: true,
                            },
                            y: {
                                stacked: true
                            }
                        },
                        legend: { display: false },
                        title: {
                            display: true,
                            text: `${player.firstname} ${player.lastname} Stats`
                        }
                    }
                });
            }
        }
    })

    async function getPlayersRequest(team, season) {
        const options = {
            method: 'GET',
            url: 'https://api-nba-v1.p.rapidapi.com/players',
            params: {
                team: team,
                season: season
            },
            headers: {
                'X-RapidAPI-Key': '8738bccd1dmsh21cc929523dd27cp1bd365jsnf795f0f34484',
                'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
            }
        };
        try {
            const response = await axios.request(options);
            return response.data.response;
        } catch (error) {
            console.error(error);
        }
    }

    // getPlayersRequest('1','2021')

    async function getPlayerStatistic(id, season) {
        const options = {
            method: 'GET',
            url: 'https://api-nba-v1.p.rapidapi.com/players/statistics',
            params: {
                id: id,
                season: season
            },
            headers: {
                'X-RapidAPI-Key': '8738bccd1dmsh21cc929523dd27cp1bd365jsnf795f0f34484',
                'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
            }
        };

        try {
            const response = await axios.request(options);
            return response.data.response;
        } catch (error) {
            console.error(error);
        }
    }

    // getPlayerStatistic('236', '2020')


    async function getTeams() {
        const options = {
            method: 'GET',
            url: 'https://api-nba-v1.p.rapidapi.com/teams',
            headers: {
                'X-RapidAPI-Key': '8738bccd1dmsh21cc929523dd27cp1bd365jsnf795f0f34484',
                'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
            }
        };

        try {
            const response = await axios.request(options);
            return response.data.response
        } catch (error) {
            console.error(error);
        }
    }

    // const barChart = new Chart(canvas, { 
    //     type: 'bar', 
    //     data: { 
    //         labels: ["bike", "car", "scooter",  
    //             "truck", "auto", "Bus"], 
    //         datasets: [{ 
    //             label: 'worst', 
    //             backgroundColor: "blue", 
    //             data: [17, 16, 4, 11, 8, 9], 
    //         }, { 
    //             label: 'Okay', 
    //             backgroundColor: "green", 
    //             data: [14, 2, 10, 6, 12, 16], 
    //         }, { 
    //             label: 'bad', 
    //             backgroundColor: "red", 
    //             data: [2, 21, 13, 3, 24, 7], 
    //         }], 
    //     }, 
    //     options: { 
    //         plugins: { 
    //             title: { 
    //                 display: true, 
    //                 text: 'Stacked Bar chart for pollution status' 
    //             }, 
    //         }, 
    //         scales: { 
    //             x: { 
    //                 stacked: true, 
    //             }, 
    //             y: { 
    //                 stacked: true 
    //             } 
    //         } 
    //     } 
    // }); 

}
