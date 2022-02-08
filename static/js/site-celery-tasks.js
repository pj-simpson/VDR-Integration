$('.dispatch-migration').on('click', function() {
    $('.dispatch-migration').hide();
  $.ajax({
    url: '/sitereplicator/',
    data: { rootFolderId: $(this).data('rootfolderid') },
    method: 'POST',
  })
  .done((res) => {
    getStatus(res.group_task_id, 'dispatch-migration');
  })
  .fail((err) => {
    console.log(err);
  });
});

$('.soft-delete').on('click', function() {
    $('.soft-delete').hide();
  $.ajax({
    url: '/sitesoftdeleter/',
    data: { rootFolderId: $(this).data('rootfolderid') },
    method: 'POST',
  })
  .done((res) => {
    getStatus(res.group_task_id,'soft-delete');
  })
  .fail((err) => {
    console.log(err);
  });
});

$('.hard-delete').on('click', function() {
    $('.hard-delete').hide();
  $.ajax({
    url: '/siteharddeleter/',
    data: { rootFolderId: $(this).data('rootfolderid') },
    method: 'POST',
  })
  .done((res) => {
    getStatus(res.group_task_id,'hard-delete');
  })
  .fail((err) => {
    console.log(err);
  });
});



function getStatus(taskID,cssClass) {
    var spinnerClass= '.spinner-site-' + cssClass;
    $(spinnerClass).show();
    $('.spinner-border').prop('disabled',true)
  $.ajax({
    url: `/tasks/${taskID}/`,
    method: 'GET'
  })
  .done((res) => {

    const taskStatus = res.group_task_success;
    if (taskStatus === 'True') {
        var originalButtonCSSClass = '.' + cssClass;
        $(spinnerClass).hide();
        $(originalButtonCSSClass).prop('disabled', true);
        $(originalButtonCSSClass).show();

        const html = `
            <div class="alert alert-success task-success" role="alert">
                All Tasks Completed Successfully! 
            </div>`
        $('.task-run-result').prepend(html);


        return false;
    }
    setTimeout(function() {
      getStatus(res.group_task_id,cssClass);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  });
}