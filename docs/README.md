The README file should be placed at the root of your project directory. This is a common practice as it ensures that anyone visiting the repository will see the README file immediately, which provides essential information about the project and how to get started.

### Steps to Add the README

1. **Navigate to the Root Directory**:
   Ensure you are in the root directory of your project (`energy-dashboard`).

   ```bash
   cd ~/Documents/Dereck_HCL/energy-dashboard
   ```

2. **Create or Edit the README.md File**:
   Create a new file named `README.md` or edit the existing one if it already exists.

   ```bash
   nano README.md
   ```

3. **Paste the README Content**:
   Copy and paste the provided README content into the `README.md` file.

4. **Save and Exit**:
   Save the changes and exit the editor. In `nano`, you can do this by pressing `CTRL+X`, then `Y` to confirm, and `Enter` to save.

5. **Commit the Changes**:
   Add and commit the `README.md` file to your repository.

   ```bash
   git add README.md
   git commit -m "Add comprehensive README for Terraform configuration"
   git push origin feature/update-terraform-configs
   ```

6. **Update the Pull Request**:
   If you have an open pull request for the `feature/update-terraform-configs` branch, the new commit will be automatically included. If not, create a pull request as described earlier.

### Final Directory Structure

Your project directory structure should look something like this:

```
energy-dashboard/
├── README.md
├── environments/
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── global/
│   ├── main.tf
│   └── variables.tf
└── modules/
    ├── network/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── vm/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```


