
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.btnn').addEventListener('click', () => {
      var message = document.querySelector('.sppiner');
      var message2 = document.querySelector('.sppiner2');
      message.style.display = 'block';
      message2.style.display = 'block';
      // message.innerHTML = 'loading...';
      setTimeout(() => {
        message.style.display = 'none';
        message2.style.display = 'none';
      }, 3000);
    });
  })
  document.addEventListener('DOMContentLoaded', () => {
  
    document.querySelector('.save').addEventListener('click', () => {
      var message = document.querySelector('.message');
      message.style.display = 'block';
      message.innerHTML = 'Saved succesfully';
      setTimeout(() => {
        message.style.display = 'none';
      }, 2000);
      window.location.href = '/';
    });
  });

  document.addEventListener('DOMContentLoaded', () => {
  
    document.querySelector('.btngpt').addEventListener('click', () => {
      var message = document.querySelector('.message');
      message.style.display = 'block';
      message.innerHTML = 'Loading...';
      setTimeout(() => {
        message.style.display = 'none';
      }, 2000);
    });
  });