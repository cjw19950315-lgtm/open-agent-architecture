"""Public Runtime API: run / resume / cancel / approve / retry / get_state / receipt."""

import os

from oaa.control import ControlPlane


class Runtime:
    def __init__(self, workspace=".", approval_mode="auto", approval_callback=None,
                 model_provider=None, base_dir=".oaa", max_workers=4):
        self.control = ControlPlane(
            workspace=workspace,
            approval_mode=approval_mode,
            approval_callback=approval_callback,
            model_provider=model_provider,
            base_dir=base_dir,
            max_workers=max_workers,
        )

    def run(self, prompt, task_id=None):
        task_id = self.control.create_task(prompt, task_id=task_id)
        self.control.plan_task(task_id)
        state = self.control.run_task(task_id)
        return {"task_id": task_id, **state}

    def resume(self, task_id):
        return self.control.resume(task_id)

    def cancel(self, task_id):
        return self.control.cancel(task_id)

    def approve(self, task_id, approved=True):
        return self.control.approve(task_id, approved=approved)

    def retry(self, task_id):
        return self.control.retry(task_id)

    def get_state(self, task_id):
        return self.control.get_state(task_id)

    def get_receipt(self, task_id):
        return self.control.get_receipt(task_id)