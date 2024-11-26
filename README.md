# DESlab Installation Guide

Welcome to the DESlab installation guide! Follow the steps below to ensure proper installation and configuration.

---

## **Prerequisites**

Before installing DESlab, make sure to complete the following steps:

1. **Install a LaTeX Distribution**  
   - Recommended: [TeXlive](https://www.tug.org/texlive/acquire.html) (also included in the `programas` folder of the DESlab package).  
   - Other distributions, such as MikTeX, should also work but may not have been fully tested.  

2. **Configure TeXlive Path**  
   - Add the path of `pdflatex.exe` from TeXlive (e.g., `C:\...\Texlive\2017\bin\win32`) to the Windows Environment Variables. See the tutorial below.

3. **Install Python 3.12**  
   - Recommended: Use the Python 3.12 installer included in the `programas` folder of the DESlab package.  
   - **Important:** During installation, ensure the checkbox to add Python to the Windows Environment Variables is selected.

4. **Remove Older Python Versions (if applicable)**  
   - If an older version of Python is installed, remove its path from the Windows Environment Variables and add the path of Python 3.12 instead. See the tutorial below.

---

## **Configuring Windows Environment Variables**

Follow these steps to configure environment variables:

1. Open the **System Properties** window:  
   - Go to **Control Panel**, select **System**, and click **Advanced System Settings**.  
   - In the **Advanced** tab, click **Environment Variables**.

2. Edit the `PATH` variable in **System Variables**:  
   - Click `Edit` and look for paths separated by `;` (semicolon).  
   - Remove the path for any older Python versions.  
   - Add the path for Python 3.12 (e.g., `C:/.../Python/Python312/`).

   **Examples**:  
   - ✅ Correct: `C:/.../Python/Python312/`  
   - ❌ Incorrect: `C:/.../Python/Python312/python.exe`

---

## **Installing DESlab**

1. Run the `Install.bat` script located in the `DESlab` folder.  
   This script will install the following software and dependencies:  
   - **Graphviz** (version 2.28)  
   - **FaDo** (version 2.2.0)  
   - **Future** (version 1.0.0)  
   - **Networkx** (version 2.8.8)  
   - **Pyparsing** (version 3.1.4)  
   - **Pydot** (version 3.0.1)  
   - **DESlab**

2. Verify the Graphviz Path:  
   - Ensure the path to Graphviz (e.g., `...Graphviz\bin`) is added to the Windows Environment Variables.

---

## **Testing the Installation**

1. Open Python IDLE and run the following commands to verify the installation:

   ```python
   from deslab import *
   syms('q1 q2 q3 a1 b1 e f')
   table = [(a1,'a_1'),(b1,'b_1'),(q1,'q_1'),(q2,'q_2'),(q3,'q_3')]
   X = [q1, q2, q3]
   Sigma = [a1, b1, e]
   X0 = [q1]
   Xm = [q3]
   T = [(q1, b1, q2), (q2, b1, q3), (q3, e, q3)]
   G1 = fsa(X, Sigma, T, X0, Xm, table, name='$G_1$')
   draw(G1)
   draw(G1, 'figurecolor')
