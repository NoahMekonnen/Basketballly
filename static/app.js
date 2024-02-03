const form = $('form')
const inputs = $('input')
form.on('submit',async function(e){
  e.preventDefault()
  console.log("HIIII")
  const games = await getRequest(inputs[1].value)

  if ($('.container')){
    $('.container').remove()
  }

  const div = $('<div class="container"></div>')

  for (let game of games){
    if (game.teams.home.name == inputs[2].value && game.teams.visitors.name == inputs[3].value){

      const xValues = [game.teams.home.name, game.teams.visitors.name]
      const yValues = [game.scores.home.points, game.scores.visitors.points]
      const barColors = ["blue", "red"]

      const barChart = new Chart("myChart", {
        type: "bar",
        data: {
          labels: xValues,
          datasets: [{
            backgroundColor: barColors,
            data: yValues
          }]
          },options: {
            legend: {display: false},
            title: {
            display: true,
            text: "Scores"
          }
        }
      });

      div.append(barChart)
      console.log(div.children)
      document.body.append(div)
    }else if (game.teams.home.name == inputs[3].value && game.teams.visitors.name == inputs[2].value){

      const xValues = [game.teams.home.name, game.teams.visitors.name]
      const yValues = [game.scores.home.points, game.scores.visitors.points]
      const barColors = ["blue", "red"]

      const barChart = new Chart("myChart", {
        type: "bar",
        data: {
          labels: xValues,
          datasets: [{
            backgroundColor: barColors,
            data: yValues
          }]
        },options: {
          legend: {display: false},
          title: {
          display: true,
          text: "Scores"
        }
      }
      });

      div.append(barChart)
      document.body.append(div)
      console.log(div)
    }
  }
  console.log(games)
})


async function getRequest(date){
  const options = {
    method: 'GET',
    url: 'https://api-nba-v1.p.rapidapi.com/games',
    params: {date: date},
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

getRequest()