function exec(){
    // Костыль из-за переопределения author с SelectMultiple на CharField
    $("#id_author").addClass("form-control")
}

$(document).ready(exec())
