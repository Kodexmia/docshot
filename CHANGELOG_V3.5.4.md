# DocShot v3.5.4 - Complete Entry Management Release

**Release Date:** November 23, 2025  
**Type:** Major Feature Release  
**Status:** Production Ready

## 🎉 What's New

### Complete Entry Management System

1. **✏️ Edit Entries** - Modify any field after creation
2. **🔢 Renumber Entries** - Reset all numbers sequentially  
3. **🗑️ Delete Entries** - Remove unwanted entries
4. **🖱️ Drag-and-Drop** - Visual reordering

## ✨ Features

- Double-click to edit entries
- Drag entries to reorder
- Keyboard shortcuts (Ctrl+Up/Down)
- Right-click context menu
- Bulk renumbering
- Delete with confirmation

## 🐛 Bug Fixes

- Fixed PyInstaller `sys.stderr` crash
- Entry ordering now persists
- Proper delete cascade

## 🔧 Technical

### New Files:
- `app/ui/draggable_entry_list.py`
- `app/ui/entry_editor.py`

### Modified:
- `app/main.py` - PyInstaller fix
- `app/core/models.py` - Added order field
- `app/core/storage.py` - Sort + delete
- `app/ui/main_window.py` - Full integration

## 📊 Complete Feature Set

✅ Create, View, Search, Filter, Export  
✅ Edit, Reorder, Renumber, Delete  

**Full lifecycle management!** 🎯
