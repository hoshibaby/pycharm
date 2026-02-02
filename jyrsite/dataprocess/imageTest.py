import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision.datasets import ImageFolder

from torchvision import datasets, transforms
from torch.utils.data import DataLoader, TensorDataset
from torchvision.utils import save_image

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'


#클래스 만들기 : cnn으로 model을 만드니까 있어야해.

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 8, 3, padding=1),
            nn.ReLU(),
            # nn.Dropout(0.25), 딥러닝 선의 25% 날려. 오버피팅 방지
            # nn.BatchNorm2d() 정규화도 가능, 1D든 2D든
            nn.MaxPool2d(kernel_size=2, stride=2)  # 64*64
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(8, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 32*32
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 16*16
        )

        self.layer4 = nn.Sequential(
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 64*8*8
        )

        self.layer5 = nn.Sequential(
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 128*4*4 만큼 특징이 있다.
        )

        # 완전 연결층

        self.fc1 = nn.Linear(128 * 4 * 4, 128)  # 128은 내 맘대로, 은닉층의 수는 모델개발자가 선택
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 5)

    def forward(self, x):  # 파이썬의 함수는 항상 self가 들어온다
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)

        # 컨볼루션 층 끝!

        # 3차원 이미지
        x = x.view(-1, 128 * 4 * 4)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        # 소프트맥스에 넣어줘야하지만 crossentropy에 넣을 거라서 바로 리턴

        return x

#함수 만들고
def image_test(file_name):
    torch.manual_seed(777)
    IMAGE_SIZE = 128

    device='cuda' if torch.cuda.is_available() else 'cpu'
    if device == 'cuda':
      torch.cuda.manual_seed_all(777)
    print(device)

#테스트 데이터 셋
    test_dataset = ImageFolder(root='static/images/', #test까지 안써도 된다.
                               transform=transforms.Compose([
                                   transforms.Resize([IMAGE_SIZE, IMAGE_SIZE]),
                                   transforms.ToTensor()
                               ])
                               )

#데이터 로드
    test_loader = DataLoader(test_dataset,
                             batch_size=10,
                             shuffle=False,
                             num_workers=1)

#이미지와 라벨을 얻음
    images, labels = next(iter(test_loader))

# 저장된 모델을 로드
    model=CNN().to(device)
    model.load_state_dict(torch.load('static/models/model.pt'))
    pred=model(images.to(device)).argmax(dim=-1)
    return pred

