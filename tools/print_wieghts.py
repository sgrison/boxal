import torch

model = torch.load('/projects/parisa/git_software/boxal/IOB_trainings/weights_warm500_itr2000_itrstep1000_eval10_loop1_initrain3089_pool200_lr0005_lrdecay5-8_batch4_roibatch512_score5_nms05_drop25_forGeneratingNewAnnotation15/exp1/random/model_final.pth')
print(model)