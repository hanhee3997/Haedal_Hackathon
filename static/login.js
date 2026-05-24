window.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast-message');

    toasts.forEach((toast, index) => {
      setTimeout(() => {
        toast.classList.add('show');
      }, 100 * index);

      setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
      }, 2600 + (index * 100));

      setTimeout(() => {
        toast.remove();
      }, 3300 + (index * 100));
    });
});