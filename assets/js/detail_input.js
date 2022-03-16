$(function () {
    $('#updateButton').click(function () {



    })

    $('a[href="#update"]').click(function () {
        $('#update').show()
        $('#nameUpdate').text($('#name'+this.id).text())
        $('#phoneUpdate').text($('#phone'+this.id).text())
        $('#stateUpdate').text($('#state'+this.id).text())
        $('#telHomeUpdate').text($('#telHome'+this.id).text())
        $('#idUpdate').val(this.id)
        $('#telWorkUpdate').text($('#telWork'+this.id).text())
        $('#commentUpdate').text($('#comment'+this.id).text())

    })
})
