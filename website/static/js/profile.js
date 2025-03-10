document.getElementById('upload').addEventListener('change', function (event) {
  const file = event.target.files[0];

  if (!file) {
    alert('Không có file nào được chọn!');
    return;
  }

  const maxSize = 1024 * 1024;
  if (file.size > maxSize) {
    alert('File vượt quá dung lượng 1024KB!');
    return;
  }

  const userId = document.getElementById('user_id').value;

  const formData = new FormData();
  formData.append('image', file);
  formData.append('user_id', userId);

  fetch('/upload', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error('Tải ảnh thất bại!');
    })
    .then((data) => {
      const uploadedAvatar = document.getElementById('uploadedAvatar');
      const newImageUrl = `../static/sneat/assets/img/avatars/${data.filename}`;
      uploadedAvatar.src = newImageUrl;
      document.getElementById('avatar_url').value = newImageUrl;
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Tải ảnh thất bại!');
    });
});


document.getElementById('resetAvatar').addEventListener('click', function (event) {
  const uploadedAvatar = document.getElementById('uploadedAvatar');
  const newImageUrl = `../static/sneat/assets/img/avatars/user.png`;
  uploadedAvatar.src = newImageUrl;
  document.getElementById('avatar_url').value = newImageUrl;
});


document.getElementById('selected_bank').addEventListener('change', function() {
  const selectedValue = this.value;
  const datalist = document.getElementById('browsers');
  const options = datalist.options;

  for (let i = 0; i < options.length; i++) {
    if (options[i].value === selectedValue) {
      document.getElementById('bank_id').value = options[i].getAttribute('data-id');
      return;
    }
  }
});