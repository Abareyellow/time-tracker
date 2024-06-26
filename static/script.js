let all = $('#all')
let vacation = $('#vaca')
let sick = $('#sick')
let rem = $('#reminder')
let urg = $('#urgent')

$('.all').on("click", displayAll)

function displayAll() {
    all.removeClass('hidden')
    vacation.addClass('hidden')
    sick.addClass('hidden')
    rem.addClass('hidden')
    urg.addClass('hidden')
}

$('.vaca').on("click", displayVaca)

function displayVaca() {
    vacation.removeClass('hidden')
    sick.addClass('hidden')
    all.addClass('hidden')
    rem.addClass('hidden')
    urg.addClass('hidden')
}

$('.sick').on("click", displaySick)

function displaySick() {
    sick.removeClass('hidden')
    vacation.addClass('hidden')
    all.addClass('hidden')
    rem.addClass('hidden')
    urg.addClass('hidden')
}

$('.reminder').on("click", displayReminder)

function displayReminder() {
    rem.removeClass('hidden')
    vacation.addClass('hidden')
    all.addClass('hidden')
    sick.addClass('hidden')
    urg.addClass('hidden')
}

$('.urgent').on("click", displayUrgent)

function displayUrgent() {
    urg.removeClass('hidden')
    rem.addClass('hidden')
    vacation.addClass('hidden')
    all.addClass('hidden')
    sick.addClass('hidden')
}

