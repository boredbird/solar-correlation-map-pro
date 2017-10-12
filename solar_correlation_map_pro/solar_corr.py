# -*- coding:utf-8 -*-
__author__ = 'boredbird'
"""
"""
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import sys

class star:
    def __init__(self,**kw):
        self.label_name = None
        self.is_planet = None # 是否为行星
        self.correlation = None # 该星与太阳的相关性
        self.planet = None  # 该卫星的行星名字
        self.moon = None    # 该行星的卫星名字
        self.orbit = None   # 所处轨道
        self.angle = None   # 与他的行星的夹角
        self.axis_x = None  # 坐标x
        self.axis_y = None  # 坐标y

        for k,v in kw.items():
            setattr(self, k, v)

    # def __init__(self):
    #     self.label_name = None
    #     self.is_planet = None # 是否为行星
    #     self.correlation = None # 该星与太阳的相关性
    #     self.planet = None  # 该卫星的行星名字
    #     self.moon = None    # 该行星的卫星名字
    #     self.orbit = None   # 所处轨道
    #     self.angle = None   # 与他的行星的夹角
    #     self.axis_x = None  # 坐标x
    #     self.axis_y = None  # 坐标y



# def __init__(self, name, gender, **kw):
#     self.name = name
#     self.gender = gender
#     for k,v in kw.items():
#         setattr(self, k, v)


# 导入数据
def load_data(filepath):
    datafile_path = filepath
    df_data = pd.read_csv(datafile_path)
    return  df_data

# 计算相似度
def compute_corr(df_data,out_path=False):
    cor_mat = np.corrcoef(df_data.T)
    df_cor = pd.DataFrame(cor_mat,columns=df_data.columns)

    if out_path:
        file_name = out_path if isinstance(out_path, str) else None
        df_cor.to_csv(file_name, index=False)

    return df_cor


# 轨道
"""
这个里面轨道并不是真正的运行轨道，只是参考辅助线。在颜色显示上需弱化。
"""

# 角度
"""
如果是行星则角度为该行星与太阳的角度；
如果是卫星则角度为该卫星与行星的角度；
"""
def get_angles(orbit, number_of_datapoints, ax):
    start = (2 * math.pi) / 11 * (orbit - 1)
    stop = start + (math.pi / 2)
    if orbit > 0:
        ax.text(0, orbit - 0.1, "{0:.1f}".format(1 - float(orbit) / 10), verticalalignment="top",
                horizontalalignment="center", color="lightgray")
    return np.linspace(start, stop, number_of_datapoints, endpoint=True)


# 获取坐标
def get_y(angle, radius):
    return math.sin(angle) * radius

def get_x(angle, radius):
    return math.cos(angle) * radius

def get_star_info(df_cor,sun):
    #todo
    stars = []

    # 初始化stars
    stars = [star(label_name=col_name) for col_name in df_data.columns]

    # 获取太阳的idx
    idx_sun = 'JEDI' == df_cor.columns

    # 先把相关系数从大到小排

    # sort_args = np.argsort(corr_dists)
    # idx_int = idx_int[sort_args]
    

    # 判断是行星还是卫星
    idx_planet = (df_cor[sun] > 0.8)&(np.logical_not(idx_sun))

    # 获取轨道

    # 获取角度

    # 获取位置

    return stars


# 画图
def plot_solar(stars,out_path=False):
    """
    stars: 类star的实例列表
    """
    if out_path:
        file_name = out_path if isinstance(out_path, str) else None
        plt.savefig(file_name)
    else:
        plt.show()


def main(filepath, sun, image_path=False):
    df_data = load_data(filepath)
    df_cor = compute_corr(df_data)
    stars = get_star_info(df_cor.fillna(0),sun)
    plot_solar(stars, out_path=image_path)


filepath = 'E:\\Code\\solar-correlation-map-pro\\jedi.csv'
sun = 'JEDI'

if __name__ == "__main__":
    try:
        image_path = sys.argv[3] if len(sys.argv) > 3 else "solar.png"
        main(sys.argv[1], sys.argv[2], image_path)
    except:
        print("python -m solar_correlation_map CSV_FILE_PATH SUN_VARIABLE [IMAGE_FILE_NAME]")
        print("example: python -m solar_correlation_map jedi.csv JEDI jedi.png")
