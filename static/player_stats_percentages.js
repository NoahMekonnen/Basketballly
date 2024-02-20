const form = $('form')
const inputs = $('input')
const canvas = document.querySelector('canvas')
console.log(form)
form[1].addEventListener('submit', async function (e) {
    e.preventDefault()
    const name = inputs[1].value
    const teamName = inputs[2].value
    const season = inputs[3].value
    let teamId;
    
    const teams = await getTeams();
    for (let team of teams) {
        if (team.name == teamName) {
            teamId = team.id
            console.log(team.name)
        }
    }
    const players = await getPlayersRequest(teamId, season)

    if ($('.container')) {
        $('.container').remove()
    }

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
            if (turnovers == 0){
                turnovers = 1
            }
            let assist_turnover_ratio = assists/turnovers
            let totalRebounds = defRebounds+offRebounds
            if (totalRebounds == 0){
                totalRebounds = 1
            }
            let offReboundRatio = offRebounds/totalRebounds
            // let avg_points = total_points/player_games.length
            let free_throw_percentage = free_throw_made / free_throw_attempted
            let three_point_percentage = three_point_made / three_point_attempted

            const xValues = ["Free Throw Percentage", "Three Point Percentage", "Assist/Turnover Ratio", "Offensive Rebound Percentage"]
            const yValues = [free_throw_percentage, three_point_percentage, assist_turnover_ratio, offReboundRatio]
            const barColors = ["blue", "red", "green","orange"]

            const barChart = new Chart(canvas, {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [{
                        backgroundColor: barColors,
                        data: yValues
                    }]
                }, options: {
                    plugins: {
                        title: {
                          display: true,
                          text: 'Chart.js Bar Chart - Stacked'
                        },
                      },
                      responsive: true,
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Scores"
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
        console.log(response.data.response)
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
        console.log(response.data);
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
        console.log(response.data);
        return response.data.response
    } catch (error) {
        console.error(error);
    }
}