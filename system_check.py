import tools.data_engine as db
import json
import os
import sys

def run_test():
    print("🚀 Shabtai XP - Self-Diagnostic System v1.0")
    print("---------------------------------------------")

    # TEST DATA
    TEST_AREA_ID = "zevah" # Assuming 'zevah' exists, or we pick the first one
    TEST_PROJECT_NAME = "__SYSTEM_TEST_PROJECT__"
    TEST_TASK_TITLE = "Test Integrity Task"

    # 1. LOAD DB
    try:
        areas = db.get_areas()
        if not isinstance(areas, list): raise ValueError("Areas is not a list")
        print("✅ [PASS] Database Loaded")
    except Exception as e:
        print(f"❌ [FAIL] Load DB: {e}")
        return

    # Ensure we have an area to work with
    if not areas:
        print("❌ [FAIL] No Areas found to test with.")
        return
    
    target_area_id = areas[0]['id'] # Use first available area

    # 2. CREATE PROJECT
    try:
        success = db.add_project(target_area_id, TEST_PROJECT_NAME)
        if not success: raise ValueError("add_project returned False")
        
        # Verify existence
        data = db.load_db()
        area = next(a for a in data['areas'] if a['id'] == target_area_id)
        project = next((p for p in area['projects'] if p['name'] == TEST_PROJECT_NAME), None)
        
        if not project: raise ValueError("Project not found in DB after creation")
        project_idx = area['projects'].index(project)
        print(f"✅ [PASS] Project Created: {TEST_PROJECT_NAME}")
    except Exception as e:
        print(f"❌ [FAIL] Create Project: {e}")
        return

    # 3. ADD TASK
    target_task_id = None
    try:
        success = db.add_task(target_area_id, project_idx, TEST_TASK_TITLE, xp=99)
        if not success: raise ValueError("add_task returned False")

        # Verify existence and ID
        data = db.load_db()
        area = next(a for a in data['areas'] if a['id'] == target_area_id)
        project = area['projects'][project_idx]
        task = next((t for t in project['tasks'] if t['title'] == TEST_TASK_TITLE), None)
        
        if not task: raise ValueError("Task not found in DB after creation")
        if task['status'] != 'todo': raise ValueError(f"Task status mismatch: {task['status']}")
        
        target_task_id = task['id']
        print(f"✅ [PASS] Task Created: {TEST_TASK_TITLE} (ID: {target_task_id})")
    except Exception as e:
        print(f"❌ [FAIL] Add Task: {e}")
        return

    # 4. COMPLETE TASK
    try:
        success = db.update_task_status(target_area_id, project_idx, target_task_id, 'complete', "Test Output")
        if not success: raise ValueError("update_task_status returned False")

        # Verify
        data = db.load_db()
        area = next(a for a in data['areas'] if a['id'] == target_area_id)
        project = area['projects'][project_idx]
        task = next(t for t in project['tasks'] if t['id'] == target_task_id)
        
        if task['status'] != 'complete': raise ValueError("Status failed to update to 'complete'")
        if 'completed_at' not in task: raise ValueError("completed_at timestamp missing")
        print("✅ [PASS] Task Completed successfully")
    except Exception as e:
        print(f"❌ [FAIL] Complete Task: {e}")
        return

    # 5. RESTORE TASK
    try:
        success = db.update_task_status(target_area_id, project_idx, target_task_id, 'process')
        if not success: raise ValueError("update_task_status returned False")

        # Verify
        data = db.load_db()
        area = next(a for a in data['areas'] if a['id'] == target_area_id)
        project = area['projects'][project_idx]
        task = next(t for t in project['tasks'] if t['id'] == target_task_id)
        
        if task['status'] != 'process': raise ValueError("Status failed to reset to 'process'")
        print("✅ [PASS] Task Restored successfully")
    except Exception as e:
        print(f"❌ [FAIL] Restore Task: {e}")
        return

    # 6. CLEANUP (DELETE)
    try:
        # Delete Task
        success = db.delete_task(target_area_id, project_idx, target_task_id)
        if not success: raise ValueError("delete_task returned False")
        
        # Check if gone
        data = db.load_db()
        area = next(a for a in data['areas'] if a['id'] == target_area_id)
        project = area['projects'][project_idx]
        task = next((t for t in project['tasks'] if t['id'] == target_task_id), None)
        if task: raise ValueError("Task still exists after delete")

        print("✅ [PASS] Cleanup: Task Deleted")
        
        # Delete Project (Cleanup the test project - doing manually to be safe or if no delete_project exists, we leave it or remove via raw logic?
        # The prompt said "Cleanup: Delete the test task and the test project"
        # Since data_engine might not have delete_project, let's implement a manual removal here or check if we can add it?
        # data_engine does NOT have delete_project exposed in recent edits.
        # We will do a raw delete here for the test script's purpose to keep DB clean.
        
        project_list = [p for p in area['projects'] if p['name'] != TEST_PROJECT_NAME]
        area['projects'] = project_list
        db.save_db(data)
        
        print("✅ [PASS] Cleanup: Project Deleted")
        
    except Exception as e:
        print(f"❌ [FAIL] Cleanup: {e}")
        return

    print("---------------------------------------------")
    print("🎉 ALL SYSTEMS OPERATIONAL")

if __name__ == "__main__":
    run_test()
