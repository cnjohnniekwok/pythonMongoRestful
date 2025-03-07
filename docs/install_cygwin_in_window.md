## Step 1: Download and Install Cygwin
1. Download the Cygwin installer

- Go to the official Cygwin website: https://www.cygwin.com

- Download the appropriate setup file

2. Run the Cygwin installer

- Double-click the downloaded setup-x86_64.exe (for 64-bit) or setup-x86.exe (for 32-bit).

- Click Next to proceed.

3. Choose an installation directory

- The default is C:\cygwin64\ for 64-bit and C:\cygwin\ for 32-bit.

- Click Next.

4. Select a download site

- Pick a mirror site from the list (e.g., http://mirrors.kernel.org/sourceware/cygwin/).

- Click Next.

## Step 2: Install Git Package in Cygwin
1. Select the packages to install

- In the package selection window, use the search bar and type git.
- Expand the Devel category.

- Locate the git package and click on Skip to select the latest version.

- Click Next.

2. Resolve dependencies and install

- Cygwin will show dependencies (if required). Click Next to confirm and start downloading.

- The installation will take some time.

3. Finish the installation

- Once installed, click Finish.

## Step 3: Verify Git Installation

### Open Cygwin Terminal

- Launch Cygwin Terminal from the Start menu.

- In the Cygwin terminal, run:

```sh
git --version
```
- If git is installed correctly, it will output something like:

```shell
git version 2.39.1
```
If you see a "command not found" error, Git is not installed or not in the PATH.

## Alternative: Run Git in Windows Command Prompt (Optional)
If you installed Git for Windows separately, you can check the version in Command Prompt (cmd.exe) or PowerShell:

```sh
git --version
```
If you only installed git via Cygwin, it will not work in Command Prompt unless Cygwin is properly added to the Windows PATH.