from mmdet.configs.maskformer.maskformer_r50_ms_16xb1_75e_coco import num_classes

_base_ = './fovea_r50_fpn_4xb4-1x_coco.py'
model = dict(
    backbone=dict(
        depth=101,
        init_cfg=dict(type='Pretrained',
                      checkpoint='torchvision://resnet101')),
    bbox_head=dict(
        num_classes=1,
        with_deform=True,
        norm_cfg=dict(type='GN', num_groups=32, requires_grad=True)))
train_pipeline = [
    dict(type='LoadImageFromFile', backend_args={{_base_.backend_args}}),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='RandomChoiceResize',
        scales=[(1333, 640), (1333, 800)],
        keep_ratio=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]
train_dataloader = dict(batch_size=8, dataset=dict(pipeline=train_pipeline))
# learning policy
max_epochs = 150
param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=500),
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_epochs,
        by_epoch=True,
        milestones=[120, 140 ],
        gamma=0.1)
]
train_cfg = dict(max_epochs=max_epochs)
load_from = '/kaggle/input/datasets/mojadoer/foveabox-large/fovea_align_r101_fpn_gn-head_mstrain_640-800_4x4_2x_coco_20200208-649c5eb6.pth'