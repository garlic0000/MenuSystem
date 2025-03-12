# 创建数据库menu_db
CREATE DATABASE menu_db;
USE menu_db;

# 菜品种类表
CREATE TABLE food_type  # 1 饮品  2 汤类  3 凉菜  4 火锅  5 炒菜
(
    `t_id`  INT PRIMARY KEY AUTO_INCREMENT,  # 菜品类型id 主键 递增
    `type_info`  VARCHAR(255)   UNIQUE NOT NULL   # 菜品类型描述 不能为空
);

# 测试数据
# 插入这些数据之后 不是递增排列
# 有问题
INSERT INTO `food_type` VALUES(1, '饮品');
INSERT INTO `food_type` VALUES(2, '汤类');
INSERT INTO `food_type` VALUES(3, '凉菜');
INSERT INTO `food_type` VALUES(4, '火锅');
INSERT INTO `food_type` VALUES(5, '炒菜');

# 菜品信息表
CREATE TABLE food_info
(
    `f_id`  INT PRIMARY KEY AUTO_INCREMENT,  # 菜品id 唯一 递增
    `f_name`    VARCHAR(255)    UNIQUE NOT NULL,  # 菜品名称 不能为空
    `price` FLOAT   NOT NULL,   # 菜品价格 不能为空
    `t_id`  INT NOT NULL ,  # 菜品种类 来自`food_type`表
    `food_info`  VARCHAR(255)    NOT NULL,   # 菜品介绍 不能为空
    `is_special` BOOL DEFAULT FALSE,   # 是否是招牌菜 默认不是
    FOREIGN KEY (`t_id`) REFERENCES `food_type` (`t_id`)  # 外键
);

# 测试数据
INSERT INTO `food_info` VALUES (1, '柠檬红茶', 3.0, 1,
                                    '具有柠檬的青酸与红茶的醇厚，茶汁微红、澄清，甜而微酸，十分爽口',
                                    FALSE);
INSERT INTO `food_info` VALUES (2, '萝卜排骨汤', 35.7, 2,
                                    '萝卜软糯，汤汁清爽温和、味道鲜美、鲜靓可口、香味浓郁、营养丰富',
                                    FALSE);
INSERT INTO `food_info` VALUES (3, '凉拌黄瓜', 14.0, 3,
                                    '香脆，爽口、酸、辣、甜、咸',
                                    FALSE);
INSERT INTO `food_info` VALUES (4, '鱼火锅', 44.0, 4,
                                    '色泽红亮，香气四溢，肉嫩味鲜，麻辣不燥',
                                    FALSE);
INSERT INTO `food_info` VALUES (5, '麻辣小龙虾', 38.9, 5,
                                    '口味麻辣鲜香，色泽红亮，质地滑嫩，滋味香辣',
                                    TRUE);




CREATE TABLE custom_info  # 顾客信息表
(
    `c_id`     INT PRIMARY KEY AUTO_INCREMENT,  # 顾客id 主键 递增
    `c_name`   VARCHAR(255) NOT NULL,  # 用户名 可以重名
    `password`  VARCHAR(255) NOT NULL,  # 用户密码
    `phone_number`  VARCHAR(255) UNIQUE NOT NULL # 手机号 唯一
);

# 测试数据
INSERT INTO `custom_info` VALUES (1, '小明', '12345', '15999034451');
INSERT INTO `custom_info` VALUES (2, '小华', '12345', '15999034452');
INSERT INTO `custom_info` VALUES (3, '花花', '12345', '15999034453');
INSERT INTO `custom_info` VALUES (4, '张三', '12345', '15999034454');
INSERT INTO `custom_info` VALUES (5, '李四', '12345', '15999034455');
INSERT INTO `custom_info` VALUES (6, '王五', '12345', '15999034456');
INSERT INTO `custom_info` VALUES (7, '小明', '12345', '13997987231');


CREATE TABLE admin_info  # 管理员信息表
(
    `a_id`     INT PRIMARY KEY AUTO_INCREMENT,  # 管理员id 主键 递增
    `a_name`   VARCHAR(255) NOT NULL ,  # 管理员登录名称
    `password` VARCHAR(255) NOT NULL  # 管理员登录密码
);

# 测试数据
INSERT INTO `admin_info` VALUES(1, '管理员', '999999999');

