let need = $("input[name='need']")
let addition = $('#addition')

need.change(function(){
    let value = $(this).val()
    //console.log(value)

    if (value == "Add") {
        addition.empty()
        addition.append("<label for='first'>First Name: <input type='text' name='first' id='first' required autocomplete='off'></label><br><label for='last'>Last Name: <input type='text' name='last' id='last' required autocomplete='off'></label>")
    } else if (value == "Update") {
        addition.empty()
        addition.append("<label for='text'> Tell us what needs to be update (Be specific)<br><textarea id='text' name='update' rows='4' cols='50'>Enter here</textarea></label>")
    } else if (value == "Other") {
        addition.empty()
        addition.append("<label for='text'> Other: <br><textarea id='text' name='update' rows='4' cols='50'>Enter here</textarea></label>")
    }
});
