<template>
  <div class="wrapper">
    <div class="container">
      <h2>我的短網址</h2>
      <div class="search-bar">
        <input
          v-model="searchTerm"
          type="text"
          class="form-control"
          placeholder="搜尋長網址、短網址、備註或使用次數"
        />
      </div>
      <table class="table table-bordered table-hover">
        <thead class="thead-dark">
          <tr>
            <th class="checkbox-column">
              <input
                type="checkbox"
                :checked="allVisibleSelected"
                ref="selectAllCheckbox"
                @change="toggleSelectAll($event.target.checked)"
                aria-label="選取當前顯示的所有短網址"
              />
            </th>
            <th>長網址</th>
            <th>短網址</th>
            <th>備註</th>
            <th>使用次數</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="url in filteredUrls" :key="url.short_id">
            <td>
              <input
                type="checkbox"
                v-model="selectedIds"
                :value="url.short_id"
                aria-label="選取短網址"
              />
            </td>
            <td>
              <a :href="url.long_url" target="_blank">{{ url.long_url }}</a>
            </td>
            <td>
              <a :href="url.short_url" target="_blank">{{ url.short_url }}</a>
            </td>
            <td class="note-column">
              <textarea v-model="url.noteDraft" class="form-control note-input" rows="2" placeholder="新增或修改備註"></textarea>
            </td>
            <td class="text-nowrap">{{ url.visit_count }}</td>
            <td>
              <div class="d-flex flex-column gap-2 align-items-center">
                <button class="btn btn-primary btn-sm" @click="updateNote(url)">更新備註</button>
                <button class="btn btn-secondary btn-sm" @click="downloadQrCode(url)">下載 QR Code</button>
                <button class="btn btn-danger btn-sm" @click="deleteUrl(url)"><p class="mb-10">刪除</p></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="chart-wrapper" v-if="hasSelected">
        <h3>使用次數圓餅圖</h3>
        <canvas ref="visitPie" aria-label="選取短網址的使用次數圓餅圖"></canvas>
      </div>
      <p v-else class="chart-placeholder">勾選表格左側方框以查看使用次數統計。</p>
    </div>
  </div>
</template>

<script>
import { nextTick } from 'vue';
import Chart from 'chart.js/auto';
import QRCode from 'qrcode';

export default {
  data() {
    return {
      urls: [],
      searchTerm: '',
      selectedIds: [],
      chartInstance: null
    };
  },
  created() {
    this.loadMyUrls();
  },
  computed: {
    filteredUrls() {
      if (!this.searchTerm.trim()) {
        return this.urls;
      }
      const keyword = this.searchTerm.trim().toLowerCase();
      return this.urls.filter((url) => {
        return [url.long_url, url.short_url, url.note, url.noteDraft, url.visit_count]
          .filter((field) => field !== null && field !== undefined)
          .some((field) => String(field).toLowerCase().includes(keyword));
      });
    },
    selectedUrls() {
      return this.urls.filter((url) => this.selectedIds.includes(url.short_id));
    },
    hasSelected() {
      return this.selectedUrls.length > 0;
    },
    allVisibleSelected() {
      if (!this.filteredUrls.length) {
        return false;
      }
      return this.filteredUrls.every((url) => this.selectedIds.includes(url.short_id));
    }
  },
  watch: {
    selectedUrls: {
      handler() {
        this.refreshChart();
        this.updateHeaderCheckboxState();
      },
      deep: true
    },
    urls: {
      handler() {
        const availableIds = this.urls.map((url) => url.short_id);
        const filteredIds = this.selectedIds.filter((id) => availableIds.includes(id));
        if (
          filteredIds.length !== this.selectedIds.length ||
          filteredIds.some((id, index) => id !== this.selectedIds[index])
        ) {
          this.selectedIds = filteredIds;
        }
        this.refreshChart();
        this.updateHeaderCheckboxState();
      },
      deep: true
    },
    filteredUrls() {
      this.updateHeaderCheckboxState();
    }
  },
  mounted() {
    this.refreshChart();
    this.updateHeaderCheckboxState();
  },
  beforeUnmount() {
    this.destroyChart();
  },
  methods: {
    async loadMyUrls() {
      try {
        const response = await fetch('http://localhost:8000/api/url/my-urls', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include'
        });
        const data = await response.json();
        if (response.ok) {
          this.urls = data.map((url) => ({
            ...url,
            visit_count: typeof url.visit_count === 'number' ? url.visit_count : 0,
            noteDraft: url.note || ''
          }));
        } else {
          alert('取得短網址列表失敗：' + (data.message || response.statusText));
        }
      } catch (error) {
        console.error('載入短網址列表錯誤:', error);
        alert('取得短網址列表時發生錯誤');
      }
    },
    async updateNote(url) {
      try {
        const response = await fetch(`http://localhost:8000/api/url/note/${url.short_id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ note: url.noteDraft })
        });
        const data = await response.json();
        if (response.ok) {
          url.note = data.note;
          url.noteDraft = data.note;
          alert('備註已更新');
        } else {
          alert('更新備註失敗：' + (data.message || response.statusText));
        }
      } catch (error) {
        console.error('更新備註錯誤:', error);
        alert('更新備註時發生錯誤');
      }
    },
    async deleteUrl(url) {
      if (!confirm('確定刪除此短網址？')) return;
      try {
        const response = await fetch(`http://localhost:8000/api/url/d/${url.short_id}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (response.ok) {
          alert('刪除成功');
          this.loadMyUrls();
        } else {
          const data = await response.json();
          alert('刪除失敗：' + (data.message || response.statusText));
        }
      } catch (error) {
        console.error('刪除錯誤:', error);
        alert('刪除短網址時發生錯誤');
      }
    },
    async downloadQrCode(url) {
      if (!url.short_url) {
        alert('找不到短網址連結，無法生成 QR Code');
        return;
      }
      try {
        const dataUrl = await QRCode.toDataURL(url.short_url, { width: 512, margin: 2 });
        const link = document.createElement('a');
        link.href = dataUrl;
        link.download = `${url.short_id || 'short-url'}-qrcode.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('產生 QR Code 錯誤:', error);
        alert('產生 QR Code 時發生錯誤');
      }
    },
    toggleSelectAll(checked) {
      if (checked) {
        const ids = this.filteredUrls.map((url) => url.short_id);
        const merged = new Set([...this.selectedIds, ...ids]);
        this.selectedIds = Array.from(merged);
      } else {
        const filteredSet = new Set(this.filteredUrls.map((url) => url.short_id));
        this.selectedIds = this.selectedIds.filter((id) => !filteredSet.has(id));
      }
    },
    refreshChart() {
      nextTick(() => {
        if (!this.hasSelected) {
          this.destroyChart();
          return;
        }

        const canvas = this.$refs.visitPie;
        if (!canvas) {
          return;
        }

        const labels = this.selectedUrls.map((url) => url.short_url || url.short_id);
        const data = this.selectedUrls.map((url) => url.visit_count || 0);
        const colors = this.generateColors(labels.length);

        if (this.chartInstance) {
          this.chartInstance.data.labels = labels;
          this.chartInstance.data.datasets[0].data = data;
          this.chartInstance.data.datasets[0].backgroundColor = colors;
          this.chartInstance.update();
          return;
        }

        this.chartInstance = new Chart(canvas.getContext('2d'), {
          type: 'pie',
          data: {
            labels,
            datasets: [
              {
                data,
                backgroundColor: colors,
                borderColor: '#ffffff',
                borderWidth: 2
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        });
      });
    },
    destroyChart() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }
    },
    generateColors(count) {
      const baseColors = [
        '#6C7A89',
        '#F5B041',
        '#A569BD',
        '#48C9B0',
        '#E74C3C',
        '#3498DB',
        '#58D68D',
        '#F4D03F'
      ];

      if (count <= baseColors.length) {
        return baseColors.slice(0, count);
      }

      const colors = [];
      for (let i = 0; i < count; i += 1) {
        colors.push(baseColors[i % baseColors.length]);
      }
      return colors;
    },
    updateHeaderCheckboxState() {
      nextTick(() => {
        const checkbox = this.$refs.selectAllCheckbox;
        if (checkbox && 'indeterminate' in checkbox) {
          checkbox.indeterminate = this.hasSelected && !this.allVisibleSelected;
        }
      });
    }
  }
};
</script>

<style scoped>
  /* 整體 wrapper 置中背景 */
  .wrapper {
    display: flex;
    justify-content: center;
    align-items: center;

    padding: 20px;
  }
  
  /* 主要容器設定 */
  .container {
    background-color: #DCD7C9;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    text-align: center;
    max-width: 800px;
    width: 100%;
  }

  .search-bar {
    margin-bottom: 20px;
  }

  /* 標題設定 */
  h2 {
    color: #2C3930;
    margin-bottom: 20px;
    font-size: 2rem;
  }
  
  /* 表格設定 */
  .table {
    background-color: #fff;
    border: none;
  }
  
  .table th,
  .table td {
    vertical-align: middle;
    text-align: center;
    padding: 15px;
  }

  .checkbox-column {
    width: 60px;
  }

  .note-column {
    min-width: 220px;
  }

  .note-input {
    resize: vertical;
  }

  /* 表頭色彩 */
  .thead-dark {
    background-color: #3F4F44;
    color: #DCD7C9;
  }
  
  /* 連結樣式 */
  a {
    color: #2C3930;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  /* 刪除按鈕 */
  .btn-danger {
    background-color: #d88268;
    border: none;
    transition: background-color 0.3s ease;
    color: white;
    border-radius: 12ch;
  }

  .btn-danger:hover {
    background-color: #3F4F44;
  }

  .btn-primary {
    background-color: #3F4F44;
    border: none;
    transition: background-color 0.3s ease;
    color: #DCD7C9;
    border-radius: 12ch;
  }

  .btn-primary:hover {
    background-color: #2C3930;
  }

  .btn-secondary {
    background-color: #6C7A89;
    border: none;
    transition: background-color 0.3s ease;
    color: #ffffff;
    border-radius: 12ch;
  }

  .btn-secondary:hover {
    background-color: #566573;
  }

  .chart-wrapper {
    margin-top: 30px;
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    min-height: 320px;
  }

  .chart-wrapper h3 {
    margin-bottom: 16px;
    color: #2C3930;
  }

  .chart-wrapper canvas {
    width: 100%;
    height: 260px;
  }

  .chart-placeholder {
    margin-top: 24px;
    color: #2C3930;
    font-style: italic;
  }
</style>
  
