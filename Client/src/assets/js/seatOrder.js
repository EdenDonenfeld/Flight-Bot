document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("container");
    const rowsContainer = document.querySelector(".rows");
    const nextButton = document.getElementById("nextButton");

    // Function to create a single row
    function createRow(rowNumber) {
        const row = document.createElement("div");
        row.classList.add("row");
        
        for (let i = 0; i < 6; i++) {
            const column = document.createElement("div");
            column.classList.add("column");

            // Setting the ID of each column to its corresponding letter (A-F)
            column.id = String.fromCharCode(65 + i) + rowNumber;

            // Creating a button for each seat
            const button = document.createElement("button");
            button.textContent = column.id;
            button.classList.add("seat");
            button.dataset.seatId = column.id;

            button.addEventListener("click", function() {
                this.classList.toggle("selected");
                // Show next button if at least one seat is selected
                nextButton.style.display = document.querySelectorAll('.selected').length > 0 ? 'block' : 'none';
            });

            column.appendChild(button);
            row.appendChild(column);
        }
        
        rowsContainer.appendChild(row);
    }

    function createRows() {
        let numberOfRows = 5;
        for (let i = 1; i <= numberOfRows; i++) {
            createRow(i);
        }
    }

    createRows();

    // Add event listener to the next button
    nextButton.addEventListener("click", function() {
        let purchasePage = "purchasePage.html"
        window.location.href = purchasePage;
    });
});
