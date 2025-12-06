<template>
  <div class="flex justify-center items-start p-6 min-h-screen">
    <div class="w-full flex flex-col items-center justify-start">
      <div
        class="bg-[#DCD7C9] p-6 rounded-xl shadow-xl text-center max-w-[800px] w-full mx-auto"
      >
        <h2 class="text-[#2C3930] mb-5 text-3xl font-bold">My Short URLs</h2>
        <div class="mb-5">
          <input
            v-model="searchTerm"
            type="text"
            class="w-full border border-gray-300 rounded p-2 focus:outline-none focus:ring-2 focus:ring-[#2C3930]"
            placeholder="Search long URL, short URL, note, visits"
          />
        </div>
        <div class="overflow-x-auto">
          <table class="w-full bg-white border-collapse">
            <thead class="bg-[#3F4F44] text-[#DCD7C9]">
              <tr>
                <th class="p-4 text-center w-[60px]">
                  <input
                    type="checkbox"
                    :checked="allVisibleSelected"
                    ref="selectAllCheckbox"
                    @change="toggleSelectAll($event.target.checked)"
                    aria-label="Select all visible short URLs"
                  />
                </th>
                <th class="p-4 text-center">Long URL</th>
                <th class="p-4 text-center">Short URL</th>
                <th class="p-4 text-center min-w-[220px]">Note</th>
                <th class="p-4 text-center">Visits</th>
                <th class="p-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="url in filteredUrls"
                :key="url.short_id"
                class="border-b border-gray-200"
              >
                <td class="p-4 text-center">
                  <input
                    type="checkbox"
                    v-model="selectedIds"
                    :value="url.short_id"
                    aria-label="Select short URL"
                  />
                </td>
                <td class="p-4 text-center break-all">
                  <a
                    :href="url.long_url"
                    target="_blank"
                    class="text-[#2C3930] hover:underline"
                    >{{ url.long_url }}</a
                  >
                </td>
                <td class="p-4 text-center">
                  <a
                    :href="url.short_url"
                    target="_blank"
                    class="text-[#2C3930] hover:underline"
                    >{{ url.short_url }}</a
                  >
                </td>
                <td class="p-4 text-center">
                  <textarea
                    v-model="url.noteDraft"
                    class="w-full border border-gray-300 rounded p-1 resize-y"
                    rows="2"
                    placeholder="Click to edit note"
                  ></textarea>
                </td>
                <td class="p-4 text-center whitespace-nowrap">
                  {{ url.visit_count }}
                </td>
                <td class="p-4 text-center">
                  <div class="flex flex-col gap-2 items-center">
                    <button
                      class="bg-[#3F4F44] text-[#DCD7C9] px-3 py-1 rounded-full hover:bg-[#2C3930] transition-colors duration-300 text-sm"
                      @click="updateNote(url)"
                    >
                      Update Note
                    </button>
                    <button
                      class="bg-[#6C7A89] text-white px-3 py-1 rounded-full hover:bg-[#566573] transition-colors duration-300 text-sm"
                      @click="downloadQrCode(url)"
                    >
                      Download QR Code
                    </button>
                    <button
                      class="bg-[#d88268] text-white px-3 py-1 rounded-full hover:bg-[#3F4F44] transition-colors duration-300 text-sm"
                      @click="deleteUrl(url)"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div
        class="mt-6 bg-white rounded-xl p-5 shadow-lg w-full max-w-[800px]"
        v-if="hasSelected"
      >
        <h3 class="mb-4 text-[#2C3930] text-xl font-bold">Visits Chart</h3>
        <VisitPieChart :items="chartItems" />
      </div>
      <p v-else class="mt-6 text-[#2C3930] italic">
        Select rows on the left to view visit statistics.
      </p>
    </div>
  </div>
</template>

<script>
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
import { nextTick } from "vue";
import QRCode from "qrcode";
import VisitPieChart from "./VisitPieChart.vue";

export default {
  components: { VisitPieChart },
  data() {
    return {
      urls: [],
      searchTerm: "",
      selectedIds: [],
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
        return [
          url.long_url,
          url.short_url,
          url.note,
          url.noteDraft,
          url.visit_count,
        ]
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
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      let letterIndex = 0;
      return this.selectedUrls.map((u) => {
        const rawNote =
          (u.note != null ? String(u.note) : "").trim() ||
          (u.noteDraft != null ? String(u.noteDraft) : "").trim();
        const label =
          rawNote && rawNote.length > 0
            ? rawNote
            : letters[letterIndex++ % letters.length];
        return {
          label,
          value: typeof u.visit_count === "number" ? u.visit_count : 0,
        };
      });
    },
    allVisibleSelected() {
      if (!this.filteredUrls.length) {
        return false;
      }
      return this.filteredUrls.every((url) =>
        this.selectedIds.includes(url.short_id)
      );
    },
  },
  watch: {
    selectedUrls: {
      handler() {
        this.updateHeaderCheckboxState();
      },
      deep: true,
    },
    urls: {
      handler() {
        const availableIds = this.urls.map((url) => url.short_id);
        const filteredIds = this.selectedIds.filter((id) =>
          availableIds.includes(id)
        );
        if (
          filteredIds.length !== this.selectedIds.length ||
          filteredIds.some((id, index) => id !== this.selectedIds[index])
        ) {
          this.selectedIds = filteredIds;
        }
        this.updateHeaderCheckboxState();
      },
      deep: true,
    },
    filteredUrls() {
      this.updateHeaderCheckboxState();
    },
  },
  mounted() {
    this.updateHeaderCheckboxState();
  },
  methods: {
    async loadMyUrls() {
      try {
        const response = await fetch(`${BASE_URL}/api/url/my-urls`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        const data = await response.json();
        if (response.ok) {
          this.urls = data.map((url) => ({
            ...url,
            visit_count:
              typeof url.visit_count === "number" ? url.visit_count : 0,
            noteDraft: url.note || "",
          }));
        } else {
          alert(
            "Failed to fetch URL list: " + (data.message || response.statusText)
          );
        }
      } catch (error) {
        console.error("Error loading URL list:", error);
        alert("An error occurred while loading URL list");
      }
    },
    async updateNote(url) {
      try {
        const response = await fetch(
          `${BASE_URL}/api/url/note/${url.short_id}`,
          {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ note: url.noteDraft }),
          }
        );
        const data = await response.json();
        if (response.ok) {
          url.note = data.note;
          url.noteDraft = data.note;
          alert("Note updated");
        } else {
          alert("Update note failed: " + (data.message || response.statusText));
        }
      } catch (error) {
        console.error("Error updating note:", error);
        alert("Note update failed");
      }
    },
    async deleteUrl(url) {
      if (!confirm("Are you sure you want to delete this short URL?")) return;
      try {
        const response = await fetch(`${BASE_URL}/api/url/d/${url.short_id}`, {
          method: "DELETE",
          credentials: "include",
        });
        if (response.ok) {
          alert("Deleted successfully");
          this.loadMyUrls();
        } else {
          const data = await response.json();
          alert("Delete failed: " + (data.message || response.statusText));
        }
      } catch (error) {
        console.error("Error deleting short URL:", error);
        alert("An error occurred while deleting");
      }
    },
    async downloadQrCode(url) {
      if (!url.short_url) {
        alert("Cannot generate QR Code: missing short URL");
        return;
      }
      try {
        const dataUrl = await QRCode.toDataURL(url.short_url, {
          width: 512,
          margin: 2,
        });
        const link = document.createElement("a");
        link.href = dataUrl;
        link.download = (url.short_id || "short-url") + "-qrcode.png";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error("QR Code generation error:", error);
        alert("QR Code generation failed");
      }
    },
    toggleSelectAll(checked) {
      if (checked) {
        const ids = this.filteredUrls.map((url) => url.short_id);
        const merged = new Set([...this.selectedIds, ...ids]);
        this.selectedIds = Array.from(merged);
      } else {
        const filteredSet = new Set(
          this.filteredUrls.map((url) => url.short_id)
        );
        this.selectedIds = this.selectedIds.filter(
          (id) => !filteredSet.has(id)
        );
      }
    },
    updateHeaderCheckboxState() {
      nextTick(() => {
        const checkbox = this.$refs.selectAllCheckbox;
        if (checkbox && "indeterminate" in checkbox) {
          checkbox.indeterminate = this.hasSelected && !this.allVisibleSelected;
        }
      });
    },
  },
};
</script>
