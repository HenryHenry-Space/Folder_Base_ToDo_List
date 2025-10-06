# Example Todo List with Tags

*Generated from folder structure: `/path/to/project`*

## Directory Structure Tasks

- [ ] **backend-#api/** `#api` `#backend`
  - [ ] **controllers/** `#endpoints`
  - [ ] **models/**
  - [ ] **services/** `#business`
- [ ] **frontend-#ui/** `#frontend` `#priority` `#ui` `#urgent`
  - [ ] **components/** `#react`
  - [ ] **pages/**
  - [ ] **styles/** `#css`
- [ ] **docs-#documentation/** `#documentation`
  - [ ] **api/**
  - [ ] **user-guide/**
- [ ] **scripts-#automation/** `#automation` `#ci`
  - [ ] **build/**
  - [ ] **deploy/** `#production`

## Tag Usage Examples

### Filtering by Tags
```bash
# Show only frontend-related directories
folder-todo-gen /path/to/project --tags frontend ui

# Show only urgent items
folder-todo-gen /path/to/project --tags urgent

# Show documentation and API related items
folder-todo-gen /path/to/project --tags documentation api
```

### Tag Sources
1. **Directory names**: Tags can be embedded in directory names using `#tag` syntax
2. **Tag files**: Create a `.tags` file in any directory with tags like `#urgent #priority`
3. **Combination**: Both methods can be used together for maximum flexibility