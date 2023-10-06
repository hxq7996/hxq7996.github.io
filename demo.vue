<div>
    <template>
      <el-button type="text" @click="outerVisible = true" class="gjs-btn animate__animated animate__pulse animate__infinite" id="i3ee9x" data-ftbuttontype="popup" data-popup="flexiPoup_5Fnah3">Register Now For FREE
        Trading Workshop</el-button>
      
      <el-dialog title="标题标题标题标题标题标题标题标题标题标题标题标题标题一" :visible.sync="outerVisible">
        
        <el-radio v-model="radio" label="1">备选项备选项备选项备选项</el-radio><br>
        <el-radio v-model="radio" label="2">备选项备选项备选项备选项</el-radio><br>
        <el-radio v-model="radio" label="3">备选项备选项备选项备选项</el-radio>
        <div slot="footer" class="dialog-footer" style="text-align: center;">
          <el-button type="primary" @click="outerVisible2 = true;outerVisible = false">打开内层 Dialog</el-button>
        </div>
      </el-dialog>
      <el-dialog title="标题标题标题标题标题标题标题标题标题标题标题标题标题二" :visible.sync="outerVisible2">
        <el-radio v-model="radio" label="1">备选项备选项备选项备选项</el-radio><br>
        <el-radio v-model="radio" label="2">备选项备选项备选项备选项</el-radio><br>
        <el-radio v-model="radio" label="3">备选项备选项备选项备选项</el-radio>
        <div slot="footer" class="dialog-footer" style="text-align: center;">
          <el-button type="primary" @click="outerVisible3 = true;outerVisible2 = false">打开内层 Dialog</el-button>
        </div>
        </el-dialog>
        <el-dialog title="标题标题标题标题标题标题标题标题标题标题标题标题标题三" :visible.sync="outerVisible3">
            <el-radio v-model="radio" label="1">备选项备选项备选项备选项</el-radio><br>
            <el-radio v-model="radio" label="2">备选项备选项备选项备选项</el-radio><br>
            <el-radio v-model="radio" label="3">备选项备选项备选项备选项</el-radio>
            <div slot="footer" class="dialog-footer" style="text-align: center;">
              <el-button type="primary" @click="outerVisible3 = false">关闭标签</el-button>
            </div>
            </el-dialog>
    </template>
    </div>
    <script>
        var Main = {
            data() {
            return {
                outerVisible: false,
                outerVisible2: false,
                outerVisible3: false,
                radio: '1'
            };
            }
        }
        var Ctor = Vue.extend(Main)
        new Ctor().$mount('#app')
    </script>