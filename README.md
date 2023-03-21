# human-segmentation

##### This dataset is split into 1700 training samples and 300 testing samples, stored in "training" and "testing" folders respectively. Each image has a unique identifier (not unique across testing and training, though) and can be used to easily retrieve its corresponding matte/segmentation. The segmentation are only binary -- foreground and background.

- dataset link: https://www.kaggle.com/datasets/tommzzhou/human-img-seg
- Example from data set:
<p float = "left">
<img src="https://storage.googleapis.com/kagglesdsdata/datasets/262654/549904/training/sample/00006.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230312%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230312T032746Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=85f41ff96750a51f65d4170c07f04e2243e9ca63a6c1c013b6e15c8265c2764d8a4e1bf32dae340202804f7a035b74e9476f8a56f9b0c3b22b7e06e5a6e58d3ea40fb1b7727f6efdadaeac4aa05846912ab18afad45b17cdce94aff25aac5950acb534baad344bbe8b13b33afc2f04c1f0cb01cdc57d5ea79511fdb3f3c6817d8facf0a3feb3c33da42f82ad64e4e9a9b710b43e6784507a5bd6477bac39ee57bdc2d719a55128b3b3986018964c75982da00cd0717aca98cad232e33d3fd4d220391cf1399dd34455e163f0ad3cc96644517a7968bb5a4455f4ea22c0af46ee6325a118175fdf23d6d3f6711274e166cb43ff00e9c773dc09e8a5e7a864d3eb" alt="sample" style="height: 400px; width:400px;"/>

<img src="https://storage.googleapis.com/kagglesdsdata/datasets/262654/549904/training/mask/00006_matte.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230312%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230312T033101Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=7efb33e9a2e83448fb6cdfc5fa015a74d03e417187d9a48f0326c804e902d75b9327aa64f619a4b1482a71e3a8710f8b8d4f401fb09e3854d2883dc5f0ef3fc1751520bb655d8fa025eb0774410258aaab2310ec60420baaad1092839b84d1ac82ad8fe792dba2c0a67bf8c2c98fee1f5af154aa9096990cb0a3a6f847a9f40aaaccbee292532587efecb7f84ed6a70b5e8256bf7f011656eb15119d4003eb0868dd81bf2767e9c67c02ef832b2d3254fb6476fb8a328c842366332181d22a42e5bc7a8d764d829069b824001155d118cdd7ead767db9b5bf730ef89cdf8a4a1bba971eb5d9a9a582ff21ed27085c26606ee954dd05368fef459e7901661b598" alt="mask" style="height: 400px; width:400px;"/>
</p>


### use deep learning for this task 
**Live demo:** https://yousef-nasr-selfie-background-remover.streamlit.app/
