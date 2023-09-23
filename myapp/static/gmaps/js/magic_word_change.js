function toggle(className, obj) {
    let $input = $(obj);
    if ($input.prop('checked')) {$(className).hide();
      document.getElementById('magic_word').value = null;
    }else{$(className).show();}
}
