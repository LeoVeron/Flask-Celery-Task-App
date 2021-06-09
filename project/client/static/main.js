// custom javascript

function handleClick() {

  var e = document.getElementById("multi-select");
  var result = e.options[e.selectedIndex].value;

  document.getElementById("result").innerHTML = "Lancement prediction".concat(' ', result);

  const words = result.split(' ');
  const id = words[2];

  fetch('/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: id }),
  })
  .then(response => response.json())
  .then(data => getStatus(data.task_id));
}

function getStatus(taskID) {
  fetch(`/tasks/${taskID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
  .then(response => response.json())
  .then(res => {
    const html = `
      <tr>
        <td>${res.match_name}</td>
        <td>${res.restime}</td>
        <td>${res.prediction}</td>
      </tr>`;
    const newRow = document.getElementById('tasks').insertRow(0);
    newRow.innerHTML = html;

    const taskStatus = res.task_status;
    if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE') return false;
    setTimeout(function() {
      getStatus(res.task_id);
    }, 1000);
  })
  .catch(err => console.log(err));
}