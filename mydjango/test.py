#coding=UTF-8

class subnav_button_data:
    def __init__(self):
        self.button_data = [
            [30, 'fulfill', '完成', 'none', 'show'],
            [20, 'move', '移至', 'dropdown', 'show'],
            [1, 'delete', '删除', 'none', 'show'],
            [4, 'delete', '删除', 'none', 'show'],
            [99, 'delete', '删除', 'none', 'show'],
            [32, 'delete', '删除', 'none', 'show'],
        ]
    
    def button_sort(self):
        id_sort_list = []
        button_data_sort = []
        
        for ids in self.button_data:
            index = self.button_data.index(ids)
            id_sort_list.append([ids[0],index])
            
        id_sort_list.sort()
        
        for ids in id_sort_list:
            button_data_sort.append(self.button_data[ids[1]])
           
        return button_data_sort
       

data = subnav_button_data()
print data.button_data
button_data_sorts = data.button_sort()
print button_data_sorts



            

