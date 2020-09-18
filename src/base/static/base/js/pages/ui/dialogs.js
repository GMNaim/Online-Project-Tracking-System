$(function () {
    $('.js-sweetalert').on('click', function () {
        let type = $(this).data('type');
        // if (type === 'basic') {
        //     showBasicMessage();
        // }
         if (type === 'with-title') {
            showWithTitleMessage();
        }
        // else if (type === 'success') {
        //     showSuccessMessage();
        // }
        if (type === 'confirm') {
            showConfirmMessage();
        }
        else if(type === 'confirm_team_delete_type'){
            showTeamDeleteConfirmMessage();
        }
        else if(type === 'confirm_department_delete'){
            showDepartmentDeleteConfirmMessage();
        }

        else if(type === 'client_delete_confirm'){
            showClientDeleteConfirmMessage();
        }

        else if(type === 'team_delete_confirm'){
            showProjectDeleteConfirmMessage();
        }

        else if(type === 'module_delete_confirm'){
            showModuleDeleteConfirmMessage();
        }
        else if(type === 'task_delete_confirm'){
            showTaskDeleteConfirmMessage();
        }





        else if (type === 'cancel') {
            showCancelMessage();
        }
        else if (type === 'with-custom-icon') {
            showWithCustomIconMessage();
        }
        else if (type === 'html-message') {
            showHtmlMessage();
        }
        else if (type === 'autoclose-timer') {
            showAutoCloseTimerMessage();
        }
        else if (type === 'prompt') {
            showPromptMessage();
        }
        else if (type === 'ajax-loader') {
            showAjaxLoaderMessage();
        }
    });
});

//These codes takes from http://t4t5.github.io/sweetalert/
// function showBasicMessage() {
//     swal("Here's a message!");
// }
//
function showWithTitleMessage() {
    swal("STOP!", "It is already assigned. You can't delete it.");
}
//
// function showSuccessMessage() {
//     swal("Good job!", "You clicked the button!", "success");
// }

function showConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Employee will be delete permanently.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_user_url;
        swal("Deleted!", "Employee has been deleted.", "success");
    });
}

function showDepartmentDeleteConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Department will be deleted permanently.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_department_url;
        swal("Deleted!", "Department has been deleted.", "success");
    });
}

function showTeamDeleteConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Team will be deleted permanently. You will lost all team members and team leader.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_team_url;
        swal("Deleted!", "Team has been deleted.", "success");
    });
}

function showClientDeleteConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Client will be deleted permanently. All projects information related with this client will be deleted.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_client_url;
        swal("Deleted!", "Client has been deleted.", "success");
    });
}


function showProjectDeleteConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Project will be deleted permanently. All information and progress of the project will be deleted.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_project_url;
        swal("Deleted!", "Project has been deleted.", "success");
    });
}


function showModuleDeleteConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Module will be deleted permanently. All information and progress of the module will be deleted.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_module_url;
        swal("Deleted!", "Module has been deleted.", "success");
    });
}

function showTaskDeleteConfirmMessage() {
    swal({
        title: "Are you sure?",
        text: "Task will be deleted permanently. All information and progress of the task will be deleted.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function () {
        window.location.href = delete_task_url;
        swal("Deleted!", "Task has been deleted.", "success");
    });
}




//
// function showWithCustomIconMessage() {
//     swal({
//         title: "STOP!",
//         text: "Task is already assigned. You can't delete it.",
//         imageUrl: "../assets/images/sm/avatar2.jpg"
//     });
// }

//
// function showCancelMessage() {
//     swal({
//         title: "Are you sure?",
//         text: "You will not be able to recover this imaginary file!",
//         type: "warning",
//         showCancelButton: true,
//         confirmButtonColor: "#dc3545",
//         confirmButtonText: "Yes, delete it!",
//         cancelButtonText: "No, cancel plx!",
//         closeOnConfirm: false,
//         closeOnCancel: false
//     }, function (isConfirm) {
//         if (isConfirm) {
//             swal("Deleted!", "Your imaginary file has been deleted.", "success");
//         } else {
//             swal("Cancelled", "Your imaginary file is safe :)", "error");
//         }
//     });
// }
//

//
// function showHtmlMessage() {
//     swal({
//         title: "HTML <small>Title</small>!",
//         text: "A custom <span style=\"color: #CC0000\">html<span> message.",
//         html: true
//     });
// }
//
// function showAutoCloseTimerMessage() {
//     swal({
//         title: "Auto close alert!",
//         text: "I will close in 2 seconds.",
//         timer: 2000,
//         showConfirmButton: false
//     });
// }
//
// function showPromptMessage() {
//     swal({
//         title: "An input!",
//         text: "Write something interesting:",
//         type: "input",
//         showCancelButton: true,
//         closeOnConfirm: false,
//         animation: "slide-from-top",
//         inputPlaceholder: "Write something"
//     }, function (inputValue) {
//         if (inputValue === false) return false;
//         if (inputValue === "") {
//             swal.showInputError("You need to write something!"); return false
//         }
//         swal("Nice!", "You wrote: " + inputValue, "success");
//     });
// }
//
// function showAjaxLoaderMessage() {
//     swal({
//         title: "Ajax request example",
//         text: "Submit to run ajax request",
//         type: "info",
//         showCancelButton: true,
//         closeOnConfirm: false,
//         showLoaderOnConfirm: true,
//     }, function () {
//         setTimeout(function () {
//             swal("Ajax request finished!");
//         }, 2000);
//     });
// }