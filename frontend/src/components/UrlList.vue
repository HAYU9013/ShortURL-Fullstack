<template>
  <div class="wrapper">
    <div class="container">
      <div class="table-section">
      <h2>My Short URLs</h2>
      <div class="search-bar">
        <input
          v-model="searchTerm"
          type="text"
          class="form-control"
          placeholder="Search long URL, short URL, note, visits"
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
                aria-label="Select all visible short URLs"
              />
            </th>
            <th>Long URL</th>
            <th>Short URL</th>
            <th>Note</th>
            <th>Visits</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="url in filteredUrls" :key="url.short_id">
            <td>
              <input
                type="checkbox"
                v-model="selectedIds"
                :value="url.short_id"
                  aria-label="Select short URL"
              />
            </td>
            <td>
              <a :href="url.long_url" target="_blank">{{ url.long_url }}</a>
            </td>
            <td>
              <a :href="url.short_url" target="_blank">{{ url.short_url }}</a>
            </td>
            <td class="note-column">
              <textarea v-model="url.noteDraft" class="form-control note-input" rows="2" placeholder="Click to edit note"></textarea>
            </td>
            <td class="text-nowrap">{{ url.visit_count }}</td>
            <td>
              <div class="d-flex flex-column gap-2 align-items-center">
                <button class="btn btn-primary btn-sm" @click="updateNote(url)">Update Note</button>
                <button class="btn btn-secondary btn-sm" @click="downloadQrCode(url)">Download QR Code</button>
                <button class="btn btn-danger btn-sm" @click="deleteUrl(url)"><p class="mb-10">Delete</p></button>
              </div>
            </td>
          </tr>
        </tbody>
        </table>
      </div>
      <div class="chart-wrapper" v-if="hasSelected">
        <h3>Visits Chart</h3>
        <VisitPieChart :items="chartItems" />
      </div>
      <p v-else class="chart-placeholder">Select rows on the left to view visit statistics.</p>
    </div>
  </div>
</template>

<script>
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
import { nextTick } from 'vue';
import QRCode from 'qrcode';
import VisitPieChart from './VisitPieChart.vue';

export default {
  components: { VisitPieChart },
  data() {
    return {
      urls: [],
      searchTerm: '',
      selectedIds: []
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
    chartItems() {
      const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      let letterIndex = 0;
      return this.selectedUrls.map((u) => {
        const rawNote = (u.note != null ? String(u.note) : '').trim() ||
                        (u.noteDraft != null ? String(u.noteDraft) : '').trim();
        const label = rawNote && rawNote.length > 0
          ? rawNote
          : letters[letterIndex++ % letters.length];
        return {
          label,
          value: typeof u.visit_count === 'number' ? u.visit_count : 0
        };
      });
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
        this.updateHeaderCheckboxState();
      },
      deep: true
    },
    filteredUrls() {
      this.updateHeaderCheckboxState();
    }
  },
  mounted() {
    this.updateHeaderCheckboxState();
  },
  methods: {
    async loadMyUrls() {
      try {
        const response = await fetch(`${BASE_URL}/api/url/my-urls`, {
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
          alert('Failed to fetch URL list: ' + (data.message || response.statusText));
        }
      } catch (error) {
        console.error('Error loading URL list:', error);
        alert('An error occurred while loading URL list');
      }
    },
    async updateNote(url) {
      try {
        const response = await fetch(`${BASE_URL}/api/url/note/${url.short_id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ note: url.noteDraft })
        });
        const data = await response.json();
        if (response.ok) {
          url.note = data.note;
          url.noteDraft = data.note;
          alert('Note updated');
        } else {
          alert('Update note failed: ' + (data.message || response.statusText));
        }
      } catch (error) {
        console.error('Error updating note:', error);
        alert('Note update failed');
      }
    },
    async deleteUrl(url) {
      if (!confirm('Are you sure you want to delete this short URL?')) return;
      try {
        const response = await fetch(`${BASE_URL}/api/url/d/${url.short_id}`, {
          method: 'DELETE',
          credentials: 'include'
        });
        if (response.ok) {
          alert('Deleted successfully');
          this.loadMyUrls();
        } else {
          const data = await response.json();
          alert('Delete failed: ' + (data.message || response.statusText));
        }
      } catch (error) {
        console.error('Error deleting short URL:', error);
        alert('An error occurred while deleting');
      }
    },
    async downloadQrCode(url) {
      if (!url.short_url) {
        alert('Cannot generate QR Code: missing short URL');
        return;
      }
      try {
        const dataUrl = await QRCode.toDataURL(url.short_url, { width: 512, margin: 2 });
        const link = document.createElement('a');
        link.href = dataUrl;
        link.download = (url.short_id || 'short-url') + '-qrcode.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('QR Code generation error:', error);
        alert('QR Code generation failed');
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
  /* Wrapper layout */
  .wrapper {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 24px;
    min-height: 100vh;
    box-sizing: border-box;
  }
  
  /* Container layout */
  .container {
    width: 100%;
    display: flex;
    flex-direction: column; /* vertical flow */
    align-items: center;    /* center content */
    justify-content: flex-start;
    box-sizing: border-box;
  }

  /* Table wrapper card */
  .table-section {
    background-color: #DCD7C9;
    padding: 24px 24px 16px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    text-align: center;
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
  }

  .search-bar {
    margin-bottom: 20px;
  }

  /* Heading */
  h2 {
    color: #2C3930;
    margin-bottom: 20px;
    font-size: 2rem;
  }
  
  /* Table */
  .table {
    background-color: #fff;
    border: none;
    margin: 0 auto; /* center table */
    width: 100%;
    table-layout: auto;
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

  /* Table header */
  .thead-dark {
    background-color: #3F4F44;
    color: #DCD7C9;
  }
  
  /* Links */
  a {
    color: #2C3930;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  /* Delete button */
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
    margin-top: 24px;
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    min-height: 320px;
    width: 100%;
    max-width: 800px;       /* cap width and center */
    box-sizing: border-box;
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
  



