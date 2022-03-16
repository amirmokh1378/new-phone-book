$(function () {

    $('#allStateCheckBox').click(function () {
        const stateCheckBoxesNo = $('.stateCheckBoxNo')
        const stateCheckBoxesYes = $('.stateCheckBoxYes')
        stateCheckBoxesNo.prop('checked', !this.checked)
        stateCheckBoxesYes.prop('checked', this.checked)


    });

    $('.stateCheckBoxNo').click(function () {
        console.log($('.stateCheckBoxYes[value="' + this.value + '"]')[0])
        $('.stateCheckBoxYes[value="' + this.value + '"]').prop('checked', !this.checked)
    });

    $('.stateCheckBoxYes').click(function () {
        console.log($('.stateCheckBoxNo[value="' + this.value + '"]')[0])
        $('.stateCheckBoxNo[value="' + this.value + '"]').prop('checked', !this.checked)
    });

    $('#changeState').click(function () {
        const allStateCheckBox = $('#allStateCheckBox')
        const saveState = $('#save')
        const states = $('.state')
        const values = $('.value')
        const stateCheckBoxesNo = $('.stateCheckBoxNo')
        const stateCheckBoxesYes = $('.stateCheckBoxYes')
        stateCheckBoxesYes.toggle(1000)
        stateCheckBoxesNo.toggle(1000)
        saveState.toggle(1000)
        states.toggle(1000)
        allStateCheckBox.toggle(1000)
        values.toggle(1000)


        for (let index = 0; index < stateCheckBoxesYes.length; index++) {
            if (states[index].innerHTML === 'بله') {
                stateCheckBoxesYes[index].checked = true
                stateCheckBoxesNo[index].checked = false
            } else {
                stateCheckBoxesYes[index].checked = false
                stateCheckBoxesNo[index].checked = true
            }

        }

    })
    $('#allDeleteCheckBox').click(function () {
        const deleteCheckBoxes = $('.deleteCheckBox')
        for (const deleteCheckBox of deleteCheckBoxes) {
            deleteCheckBox.checked = this.checked
        }
    })
    const states = $('.state')
    const stateCheckBoxesNo = $('.stateCheckBoxNo')
    const stateCheckBoxesYes = $('.stateCheckBoxYes')

    for (let index = 0; index < stateCheckBoxesYes.length; index++) {
        if (states[index].innerHTML === 'بله') {
            stateCheckBoxesYes[index].setAttribute('checked', 'checked')
            stateCheckBoxesNo[index].removeAttribute('checked', 'checked')
        } else {
            stateCheckBoxesYes[index].removeAttribute('checked', 'checked')
            stateCheckBoxesNo[index].setAttribute('checked', 'checked')
        }

    }
});
