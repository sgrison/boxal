import os
from detectron2.engine.hooks import LossEvalHook, BestCheckpointer
from detectron2.evaluation import COCOEvaluator
from detectron2.engine import DefaultTrainer
from detectron2.data import DatasetMapper, build_detection_test_loader

__all__ = ["CustomTrainer",]

class CustomTrainer(DefaultTrainer):
    '''
    cutom trainer class to write validation loss as output. This is not done by the default trainer.
    '''
    def __init__(self, cfg, iter, val_value, metric):
        super().__init__(cfg)
        self.iter = iter
        self.val_value = val_value
        self.metric = metric

    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        if output_folder is None:
            output_folder = os.path.join(cfg.OUTPUT_DIR, "inference")
        return COCOEvaluator(dataset_name, {"bbox"}, False, output_dir=output_folder)

    def build_hooks(self):
        hooks = super().build_hooks()
        hooks.insert(-1, BestCheckpointer(
            self.iter,
            self.cfg.TEST.EVAL_PERIOD,
            self.val_value,
            self.metric))
        hooks.insert(-1, LossEvalHook(
            self.cfg.TEST.EVAL_PERIOD,
            self.model,
            build_detection_test_loader(
                self.cfg,
                self.cfg.DATASETS.TEST[0],
                DatasetMapper(self.cfg,True))
            ))
        return hooks
