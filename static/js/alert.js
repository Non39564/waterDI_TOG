function alert() {
  $.getJSON("/dataapi").done(function (json) {
    var toastLiveExample = document.getElementById("liveToast");
    for (i in json) {
      const d = new Date();
      const day = d.getDate();
      const month = d.getMonth() + 1;
      const year = d.getFullYear();
      const h = d.getHours();
      const m = d.getMinutes();
      if (m < 10) {
        const m = "0" + m;
        console.log(m);
      }
      const erroralert = [];
      for (j in json[i].Data) {
        if (json[i].Data[j].Water < 5) {
          var toast = new bootstrap.Toast(toastLiveExample);
          var macName = json[i].Data[j].id;
          erroralert.push(macName);
        }
      }
      if (erroralert.length > 0) {
        document.getElementById("AlertId").innerHTML =
          "Di Error<br> " + erroralert.join(" <br> ");
        document.getElementById("timealert").innerHTML =
          day + "/" + month + "/" + year + "          " + h + ":" + m;
        toast.show();
      }
    }
  });
}
setInterval(alert, 1000);

function AlertsLogin() {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: "Password or Username went wrong!",
  });
}

function AlertAddError() {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: "Phase or Name is not correct!",
  });
}
function AlertAddSuccess() {
  Swal.fire({
    icon: "success",
    title: "success",
    text: "Your machine has been added",
  });
}
function AlertDeleteError() {
  Swal.fire({
    icon: "error",
    title: "Error!",
    text: "Phase or Name is not correct!",
  });
}
function AlertDeleteSuccess() {
  Swal.fire({
    icon: "success",
    title: "success",
    text: "Your machine has been deleted",
  });
}
function AlertNotMatchPassword() {
  Swal.fire({
    icon: "error",
    title: "Error!",
    text: "Password Not Matching!",
  });
}
function AlertWaitRecept() {
  Swal.fire({
    icon: "success",
    title: "success",
    text: "Wait for recept",
  });
}
$( ".delete" ).click(function() {
  Swal.fire({
    title: "Are you sure?",
    text: "You want delete this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire("Deleted!", "Your device has been deleted.", "success").then(
        (result) => {
          if (result.isConfirmed) {
            window.location.href = "delete?Site=" + $(this).val();
          }
        }
      );
    }
  });
});