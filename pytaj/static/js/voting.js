//upvote and downvote script
var csrftoken = window.Cookies.get("csrftoken");
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  },
});
function refresh_score(answerid) {
  $("#score-" + answerid).load(
    window.location.href + " " + "#score-" + answerid
  );
}
$(".upvote").click(function () {
  let answerid = $(this).data("answer-id");
  let second_vote = $(this).hasClass("is-upvoted");
  if (!second_vote) {
    $.post("/answer/upvote", { answer_id: answerid }, function (response) {
      refresh_score(answerid);
      $("#downvote-" + answerid).removeClass("is-downvoted");
      $("#upvote-" + answerid).addClass("is-upvoted");
    });
  } else {
    $.post("/answer/unvote", { answer_id: answerid }, function (response) {
      refresh_score(answerid);
      $("#upvote-" + answerid).removeClass("is-upvoted");
    });
  }
});

$(".downvote").click(function () {
  let answerid = $(this).data("answer-id");
  let second_vote = $(this).hasClass("is-downvoted");
  if (!second_vote) {
    $.post("/answer/downvote", { answer_id: answerid }, function (response) {
      refresh_score(answerid);
      $("#upvote-" + answerid).removeClass("is-upvoted");
      $("#downvote-" + answerid).addClass("is-downvoted");
    });
  } else {
    $.post("/answer/unvote", { answer_id: answerid }, function (response) {
      refresh_score(answerid);
      $("#downvote-" + answerid).removeClass("is-downvoted");
    });
  }
});
