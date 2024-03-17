const form = $('form')
const inputs = $('input')
const canvas = document.querySelector('canvas')
console.log(form,"FORM")
form.on('submit', async function (e) {
  e.preventDefault()
  team = inputs[1].value
  const games = await getGameRequest(team)

  if ($('.container')) {
    $('.container').remove()
  }

  for (let game of games) {
    console.log(game.teams.home.name, inputs[2].value, game.teams.visitors.name, inputs[3].value)
    if (game.teams.home.name == inputs[2].value && game.teams.visitors.name == inputs[3].value) {

      const xValues = [game.teams.home.name, game.teams.visitors.name]
      const yValues = [game.scores.home.points, game.scores.visitors.points]
      const barColors = ["blue", "red"]

      const barChart = new Chart(canvas, {
        type: "bar",
        data: {
          labels: xValues,
          datasets: [{
            backgroundColor: barColors,
            data: yValues
          }]
        }, options: {

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
    } else if (game.teams.home.name == inputs[3].value && game.teams.visitors.name == inputs[2].value) {

      const xValues = [game.teams.home.name, game.teams.visitors.name]
      const yValues = [game.scores.home.points, game.scores.visitors.points]
      const barColors = ["blue", "red"]

      const barChart = new Chart(canvas, {
        type: "bar",
        data: {
          labels: xValues,
          datasets: [{
            backgroundColor: barColors,
            data: yValues
          }]
        }, options: {

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
  console.log(games)
})


async function getGameRequest(date) {
  const options = {
    method: 'GET',
    url: 'https://api-nba-v1.p.rapidapi.com/games',
    params: { date: date },
    headers: {
      'X-RapidAPI-Key': '8738bccd1dmsh21cc929523dd27cp1bd365jsnf795f0f34484',
      'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
    }
  };
  try {
    const response = await axios.request(options);
    console.log(response)
    return response.data.response;
  } catch (error) {
    console.error(error);
  }
}

async function testRequest(){
  const options = {
    method: 'GET',
    url: 'https://api-nba-v1.p.rapidapi.com/games',
    params: {h2h: '1-2'},
    headers: {
      'X-RapidAPI-Key': '8738bccd1dmsh21cc929523dd27cp1bd365jsnf795f0f34484',
      'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'
    }
  };
  
  try {
    const response = await axios.request(options);
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
}

// testRequest()