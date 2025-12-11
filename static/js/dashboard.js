document.addEventListener("DOMContentLoaded", function () {
  const { expenseData, loanData, insuranceData, categoryData } = window.dashboardData;

  const colorPalette = [
    "rgba(255, 99, 132, 0.8)",   // Red
    "rgba(54, 162, 235, 0.8)",   // Blue
    "rgba(255, 206, 86, 0.8)",   // Yellow
    "rgba(75, 192, 192, 0.8)",   // Teal
    "rgba(153, 102, 255, 0.8)",  // Purple
    "rgba(255, 159, 64, 0.8)",   // Orange
    "rgba(199, 199, 199, 0.8)",  // Grey
    "rgba(255, 99, 255, 0.8)",   // Pink
    "rgba(99, 255, 132, 0.8)",   // Green
    "rgba(255, 215, 0, 0.8)",    // Gold
    "rgba(0, 128, 128, 0.8)"     // Dark Teal
  ];

  // Function to render small charts (do not open modal)
  function renderSmallChart(ctx, type, label, data, borderColor) {
    return new Chart(ctx, {
      type: type,
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          label: label,
          data: data.map(d => d.value),
          borderColor: borderColor,
          backgroundColor: type === "pie" ? colorPalette : borderColor,
          fill: false,
          tension: 0.1
        }]
      },
      options: {
        plugins: {
          legend: { display: type !== "line" || type !== "bar" }
        }
      }
    });
  }

  // Render small charts
  renderSmallChart(document.getElementById("expenseChart"), "line", "Expenses", expenseData, "rgba(75,192,192,1)");
  renderSmallChart(document.getElementById("loanChart"), "line", "Loan Amounts", loanData, "rgba(255,99,132,1)");
  renderSmallChart(document.getElementById("insuranceChart"), "line", "Premiums", insuranceData, "rgba(54,162,235,1)");
  renderSmallChart(document.getElementById("categoryChart"), "pie", "Categories", categoryData, "rgba(255,206,86,1)");

  // Click to open modal with bigger chart
  function showChartModal(chartType, type, label, data, borderColor) {
    const modal = document.getElementById("chartDetailModal");
    const modalTitle = modal.querySelector(".modal-title");
    const modalBody = modal.querySelector(".modal-body");

    const titles = {
      'expense': 'Monthly Expenses Chart',
      'loan': 'Loans by Year Chart',
      'insurance': 'Insurance Premiums Chart',
      'category': 'Expenses by Category Chart'
    };

    modalTitle.textContent = titles[chartType];

    // Clear modal content and create new canvas
    modalBody.innerHTML = `<canvas id="modalChart" style="width:100%; height:400px;"></canvas>`;
    const modalCtx = document.getElementById("modalChart").getContext("2d");

    // Render bigger chart in modal
    new Chart(modalCtx, {
      type: type,
      data: {
        labels: data.map(d => d.label),
        datasets: [{
          label: label,
          data: data.map(d => d.value),
          borderColor: borderColor,
          backgroundColor: type === "pie" ? colorPalette : borderColor,
          fill: false,
          tension: 0.1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    });

    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
  }

  // Add click handlers for all charts
  document.getElementById("viewExpenseChartBtn").addEventListener("click", () =>
    showChartModal("expense", "line", "Expenses", expenseData, "rgba(75,192,192,1)")
  );
  document.getElementById("viewLoanChartBtn").addEventListener("click", () =>
    showChartModal("loan", "line", "Loan Amounts", loanData, "rgba(255,99,132,1)")
  );
  document.getElementById("viewInsuranceChartBtn").addEventListener("click", () =>
    showChartModal("insurance", "line", "Premiums", insuranceData, "rgba(54,162,235,1)")
  );
  document.getElementById("viewCategoryChartBtn").addEventListener("click", () =>
    showChartModal("category", "pie", "Categories", categoryData, "rgba(255,206,86,1)")
  );
});

// Custom scrollbar
document.addEventListener('DOMContentLoaded', function() {
  const scrollbarThumb = document.getElementById('customScrollbarThumb');
  const scrollbarContainer = document.querySelector('.custom-scrollbar-container');

  function updateScrollbar() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercentage = (scrollTop / scrollHeight) * 100;
    const thumbHeight = Math.max(20, (document.documentElement.clientHeight / document.documentElement.scrollHeight) * 100);

    scrollbarThumb.style.height = thumbHeight + '%';
    scrollbarThumb.style.top = scrollPercentage + '%';

    scrollbarContainer.style.display = scrollHeight <= 0 ? 'none' : 'block';
  }

  window.addEventListener('scroll', updateScrollbar);
  window.addEventListener('resize', updateScrollbar);

  scrollbarThumb.addEventListener('click', e => e.preventDefault());

  scrollbarContainer.addEventListener('click', function(e) {
    const rect = scrollbarContainer.getBoundingClientRect();
    const clickY = e.clientY - rect.top;
    const scrollPercentage = (clickY / rect.height) * 100;
    const scrollTop = (scrollPercentage / 100) * (document.documentElement.scrollHeight - document.documentElement.clientHeight);
    window.scrollTo({ top: scrollTop, behavior: 'smooth' });
  });

  updateScrollbar();
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".modal").forEach(modal => {

    modal.addEventListener("hidden.bs.modal", function () {

      const returnTo = modal.getAttribute("data-return");

      if (!returnTo) return; // ignore modals with no return target

      // prevent infinite loop if graph modal is already open
      const alreadyOpen = document.getElementById(returnTo).classList.contains("show");
      if (alreadyOpen) return;

      setTimeout(() => {
        const modalObj = new bootstrap.Modal(document.getElementById(returnTo));
        modalObj.show();
      }, 200); // slight delay for smooth animation
    });

  });
});
