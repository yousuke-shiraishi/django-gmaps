$(document).ready(function() {
  let flag = true;

  $(".radio input[type=radio]").change(function() {
    flag = !flag;
    if (flag === true) {
      $("#form1").show();
      $("#form2").hide();
    } else {
      $("#form2").show();
      $("#form1").hide();
    }
  });
});
