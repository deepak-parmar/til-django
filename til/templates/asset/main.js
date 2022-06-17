$.ajaxSetup({
  // headers: {
  //   "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
  // },
  beforeSend: function beforeSend(xhr, settings) {
    function getCookie(name) {
      let cookieValue = null;

      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i += 1) {
          const cookie = jQuery.trim(cookies[i]);

          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === `${name}=`) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }

      return cookieValue;
    }

    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
  },
});

$("#js-create-post-form").submit((event) => {
  event.preventDefault();
  const content = $("#id_content").val().trim();

  $.ajax({
    url: "/post/",
    method: "POST",
    data: {
      content: content,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    beforeSend: () => {
      $("#id_content").val("");
      $("#js-create-post-form button[type=submit]").prop("disabled", true);
    },
  })
    .done((response) => {
      // inject new post
      $("#js-create-post-form").slideToggle();
      $(".js-post-container").prepend(response);
    })
    .fail((error) => {
      console.warn("problem happened: ", error);
    });
});

$("#menuBtn").click(function () {
  $(".js-navbar").toggleClass("-ml-56");
});

$("#navPostBtn").click(() => {
  $("#js-create-post-form").slideToggle();
});

$("#id_content").keyup(function () {
  const contentLength = $(this).val().length;
  contentLength
    ? $("#js-create-post-form button[type=submit]").prop("disabled", false)
    : $("#js-create-post-form button[type=submit]").prop("disabled", true);
});

$(".js-follow").click(function (event) {
  event.preventDefault();
  const action = $(this).attr("data-action");

  $.ajax({
    type: "POST",
    url: $(this).data("url"),
    data: {
      action: action,
      username: $(this).data("username"),
    },
    success: (data) => {
      $(this).text(data.buttonLabel);
      if (action == "follow") {
        $(this).attr("data-action", "unfollow");
      } else {
        $(this).attr("data-action", "follow");
      }
    },
    error: (error) => {
      console.warn(error);
    },
  });
});
