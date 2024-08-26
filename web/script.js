eel.new_day();

eel.expose(update_tiles);
function update_tiles(table, current_prayer) {
  var before = 1;
  for (var key in table) {
    var e = document.getElementById(key);
    e.innerHTML = table[key];
    if (key == current_prayer) {
      e.parentElement.parentElement.style.backgroundColor = "#75A297";
      before = 0;
    } else if (before == 1) {
      e.parentElement.parentElement.style.backgroundColor = "#FF4E60";
    } else {
      e.parentElement.parentElement.style.backgroundColor = "#E3AE7A";
    }
  }
}

eel.expose(set_time_remaining);
function set_time_remaining(t) {
  document.getElementById("time-remaining").innerHTML = t;
}

eel.expose(set_time);
function set_time(t) {
  document.getElementById("time").innerHTML = t;
}

eel.expose(set_date);
function set_date(t) {
  document.getElementById("date").innerHTML = t;
}
